from flask import render_template, request, redirect, url_for, flash, jsonify, send_file
from app import app, db
from models import Customer, Contact, Appointment, Document
from datetime import datetime, timedelta
from sqlalchemy import or_, func
import os
import uuid
from werkzeug.utils import secure_filename

# Upload configuration
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'doc', 'docx', 'xls', 'xlsx', 'ppt', 'pptx'}
MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_LENGTH

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    search = request.args.get('search', '')
    category = request.args.get('category', '')
    sort_by = request.args.get('sort_by', 'updated_at')
    order = request.args.get('order', 'desc')
    
    query = Customer.query
    
    # Apply search filter
    if search:
        query = query.filter(
            or_(
                Customer.company_name.ilike(f'%{search}%'),
                Customer.industry.ilike(f'%{search}%'),
                Customer.city.ilike(f'%{search}%')
            )
        )
    
    # Apply category filter
    if category:
        query = query.filter(Customer.category == category)
    
    # Apply sorting
    if sort_by == 'company_name':
        if order == 'asc':
            query = query.order_by(Customer.company_name.asc())
        else:
            query = query.order_by(Customer.company_name.desc())
    elif sort_by == 'created_at':
        if order == 'asc':
            query = query.order_by(Customer.created_at.asc())
        else:
            query = query.order_by(Customer.created_at.desc())
    else:  # updated_at
        if order == 'asc':
            query = query.order_by(Customer.updated_at.asc())
        else:
            query = query.order_by(Customer.updated_at.desc())
    
    customers = query.all()
    
    # Get category statistics
    category_stats = db.session.query(
        Customer.category,
        func.count(Customer.id).label('count')
    ).group_by(Customer.category).all()
    
    stats = {stat.category: stat.count for stat in category_stats}
    
    # Get upcoming appointments for each customer
    customer_appointments = {}
    for customer in customers:
        upcoming_appointments = db.session.query(Appointment)\
            .join(Contact)\
            .filter(Contact.customer_id == customer.id)\
            .filter(Appointment.appointment_date >= datetime.now())\
            .order_by(Appointment.appointment_date.asc())\
            .limit(3).all()
        customer_appointments[customer.id] = upcoming_appointments
    
    return render_template('index.html', 
                         customers=customers, 
                         search=search, 
                         category=category,
                         sort_by=sort_by,
                         order=order,
                         stats=stats,
                         customer_appointments=customer_appointments)

@app.route('/customer/new', methods=['GET', 'POST'])
def new_customer():
    if request.method == 'POST':
        customer = Customer(
            company_name=request.form['company_name'],
            industry=request.form.get('industry'),
            address=request.form.get('address'),
            city=request.form.get('city'),
            postal_code=request.form.get('postal_code'),
            country=request.form.get('country'),
            website=request.form.get('website'),
            category=request.form.get('category', 'neu'),
            notes=request.form.get('notes')
        )
        
        try:
            db.session.add(customer)
            db.session.commit()
            flash('Kunde erfolgreich erstellt!', 'success')
            return redirect(url_for('customer_detail', id=customer.id))
        except Exception as e:
            db.session.rollback()
            flash(f'Fehler beim Erstellen des Kunden: {str(e)}', 'error')
    
    return render_template('customer_form.html')

@app.route('/customer/<int:id>')
def customer_detail(id):
    customer = Customer.query.get_or_404(id)
    
    # Get upcoming appointments for this customer
    upcoming_appointments = db.session.query(Appointment)\
        .join(Contact)\
        .filter(Contact.customer_id == id)\
        .filter(Appointment.appointment_date >= datetime.now())\
        .order_by(Appointment.appointment_date.asc())\
        .limit(5).all()
    
    return render_template('customer_detail.html', 
                         customer=customer,
                         upcoming_appointments=upcoming_appointments)

@app.route('/customer/<int:id>/edit', methods=['GET', 'POST'])
def edit_customer(id):
    customer = Customer.query.get_or_404(id)
    
    if request.method == 'POST':
        customer.company_name = request.form['company_name']
        customer.industry = request.form.get('industry')
        customer.address = request.form.get('address')
        customer.city = request.form.get('city')
        customer.postal_code = request.form.get('postal_code')
        customer.country = request.form.get('country')
        customer.website = request.form.get('website')
        customer.category = request.form.get('category', 'neu')
        customer.notes = request.form.get('notes')
        customer.updated_at = datetime.utcnow()
        
        try:
            db.session.commit()
            flash('Kunde erfolgreich aktualisiert!', 'success')
            return redirect(url_for('customer_detail', id=customer.id))
        except Exception as e:
            db.session.rollback()
            flash(f'Fehler beim Aktualisieren des Kunden: {str(e)}', 'error')
    
    return render_template('customer_form.html', customer=customer, now=datetime.now())

@app.route('/customer/<int:id>/delete', methods=['POST'])
def delete_customer(id):
    customer = Customer.query.get_or_404(id)
    
    try:
        db.session.delete(customer)
        db.session.commit()
        flash('Kunde erfolgreich gelöscht!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Fehler beim Löschen des Kunden: {str(e)}', 'error')
    
    return redirect(url_for('index'))

@app.route('/customer/<int:id>/print')
def print_customer(id):
    customer = Customer.query.get_or_404(id)
    return render_template('customer_print.html', customer=customer)

@app.route('/customer/<int:id>/print-edit')
def print_customer_edit(id):
    customer = Customer.query.get_or_404(id)
    return render_template('customer_edit_print.html', customer=customer, now=datetime.now())

@app.route('/customer/<int:customer_id>/contact/new', methods=['GET', 'POST'])
def new_contact(customer_id):
    customer = Customer.query.get_or_404(customer_id)
    
    if request.method == 'POST':
        contact = Contact(
            customer_id=customer_id,
            first_name=request.form['first_name'],
            last_name=request.form['last_name'],
            title=request.form.get('title'),
            email=request.form.get('email'),
            phone=request.form.get('phone'),
            mobile=request.form.get('mobile'),
            department=request.form.get('department'),
            is_primary=bool(request.form.get('is_primary')),
            notes=request.form.get('notes')
        )
        
        try:
            db.session.add(contact)
            db.session.commit()
            flash('Ansprechpartner erfolgreich erstellt!', 'success')
            return redirect(url_for('customer_detail', id=customer_id))
        except Exception as e:
            db.session.rollback()
            flash(f'Fehler beim Erstellen des Ansprechpartners: {str(e)}', 'error')
    
    return render_template('contact_form.html', customer=customer)

@app.route('/contact/<int:id>/edit', methods=['GET', 'POST'])
def edit_contact(id):
    contact = Contact.query.get_or_404(id)
    
    if request.method == 'POST':
        contact.first_name = request.form['first_name']
        contact.last_name = request.form['last_name']
        contact.title = request.form.get('title')
        contact.email = request.form.get('email')
        contact.phone = request.form.get('phone')
        contact.mobile = request.form.get('mobile')
        contact.department = request.form.get('department')
        contact.is_primary = bool(request.form.get('is_primary'))
        contact.notes = request.form.get('notes')
        contact.updated_at = datetime.utcnow()
        
        try:
            db.session.commit()
            flash('Ansprechpartner erfolgreich aktualisiert!', 'success')
            return redirect(url_for('customer_detail', id=contact.customer_id))
        except Exception as e:
            db.session.rollback()
            flash(f'Fehler beim Aktualisieren des Ansprechpartners: {str(e)}', 'error')
    
    return render_template('contact_form.html', contact=contact, customer=contact.customer, now=datetime.now())

@app.route('/contact/<int:id>/delete', methods=['POST'])
def delete_contact(id):
    contact = Contact.query.get_or_404(id)
    customer_id = contact.customer_id
    
    try:
        db.session.delete(contact)
        db.session.commit()
        flash('Ansprechpartner erfolgreich gelöscht!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Fehler beim Löschen des Ansprechpartners: {str(e)}', 'error')
    
    return redirect(url_for('customer_detail', id=customer_id))

@app.route('/contact/<int:contact_id>/appointment/new', methods=['GET', 'POST'])
def new_appointment(contact_id):
    contact = Contact.query.get_or_404(contact_id)
    
    if request.method == 'POST':
        appointment_datetime = datetime.strptime(
            f"{request.form['appointment_date']} {request.form['appointment_time']}", 
            '%Y-%m-%d %H:%M'
        )
        
        appointment = Appointment(
            contact_id=contact_id,
            title=request.form['title'],
            description=request.form.get('description'),
            appointment_date=appointment_datetime,
            duration_minutes=int(request.form.get('duration_minutes', 60)),
            location=request.form.get('location'),
            appointment_type=request.form.get('appointment_type', 'meeting'),
            notes=request.form.get('notes')
        )
        
        try:
            db.session.add(appointment)
            db.session.commit()
            flash('Termin erfolgreich erstellt!', 'success')
            
            # Check if we came from contact edit page
            referrer = request.referrer
            from_contact_edit = referrer and 'contact' in referrer and 'edit' in referrer
            
            if from_contact_edit:
                return redirect(url_for('edit_contact', id=contact_id))
            else:
                return redirect(url_for('customer_detail', id=contact.customer_id))
        except Exception as e:
            db.session.rollback()
            flash(f'Fehler beim Erstellen des Termins: {str(e)}', 'error')
    
    return render_template('appointment_form.html', contact=contact)

@app.route('/appointment/<int:id>/edit', methods=['GET', 'POST'])
def edit_appointment(id):
    appointment = Appointment.query.get_or_404(id)
    
    if request.method == 'POST':
        appointment_datetime = datetime.strptime(
            f"{request.form['appointment_date']} {request.form['appointment_time']}", 
            '%Y-%m-%d %H:%M'
        )
        
        appointment.title = request.form['title']
        appointment.description = request.form.get('description')
        appointment.appointment_date = appointment_datetime
        appointment.duration_minutes = int(request.form.get('duration_minutes', 60))
        appointment.location = request.form.get('location')
        appointment.appointment_type = request.form.get('appointment_type', 'meeting')
        appointment.status = request.form.get('status', 'scheduled')
        appointment.notes = request.form.get('notes')
        appointment.updated_at = datetime.utcnow()
        
        try:
            db.session.commit()
            flash('Termin erfolgreich aktualisiert!', 'success')
            
            # Check if we came from contact edit page
            referrer = request.referrer
            from_contact_edit = referrer and 'contact' in referrer and 'edit' in referrer
            
            if from_contact_edit:
                return redirect(url_for('edit_contact', id=appointment.contact_id))
            else:
                return redirect(url_for('customer_detail', id=appointment.contact.customer_id))
        except Exception as e:
            db.session.rollback()
            flash(f'Fehler beim Aktualisieren des Termins: {str(e)}', 'error')
    
    return render_template('appointment_form.html', appointment=appointment, contact=appointment.contact)

@app.route('/appointment/<int:id>/delete', methods=['POST'])
def delete_appointment(id):
    appointment = Appointment.query.get_or_404(id)
    contact_id = appointment.contact_id
    customer_id = appointment.contact.customer_id
    
    # Check if we came from contact edit page
    referrer = request.referrer
    from_contact_edit = referrer and 'contact' in referrer and 'edit' in referrer
    
    try:
        db.session.delete(appointment)
        db.session.commit()
        flash('Termin erfolgreich gelöscht!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Fehler beim Löschen des Termins: {str(e)}', 'error')
    
    # If we came from contact edit page, redirect back there
    if from_contact_edit:
        return redirect(url_for('edit_contact', id=contact_id))
    else:
        return redirect(url_for('customer_detail', id=customer_id))

@app.route('/categories')
def categories():
    # Get detailed category statistics
    category_stats = db.session.query(
        Customer.category,
        func.count(Customer.id).label('count')
    ).group_by(Customer.category).all()
    
    # Get customers by category
    customers_by_category = {}
    for category, count in category_stats:
        customers_by_category[category] = Customer.query.filter_by(category=category).order_by(Customer.updated_at.desc()).limit(5).all()
    
    total_customers = Customer.query.count()
    
    return render_template('categories.html', 
                         category_stats=category_stats,
                         customers_by_category=customers_by_category,
                         total_customers=total_customers)

@app.route('/api/customer/<int:id>')
def api_customer(id):
    customer = Customer.query.get_or_404(id)
    
    # Convert customer to dict
    customer_data = {
        'id': customer.id,
        'company_name': customer.company_name,
        'industry': customer.industry,
        'address': customer.address,
        'city': customer.city,
        'postal_code': customer.postal_code,
        'country': customer.country,
        'website': customer.website,
        'category': customer.category,
        'notes': customer.notes,
        'created_at': customer.created_at.isoformat(),
        'updated_at': customer.updated_at.isoformat(),
        'contacts': []
    }
    
    # Add contacts and appointments
    for contact in customer.contacts:
        contact_data = {
            'id': contact.id,
            'full_name': contact.full_name,
            'first_name': contact.first_name,
            'last_name': contact.last_name,
            'title': contact.title,
            'email': contact.email,
            'phone': contact.phone,
            'mobile': contact.mobile,
            'department': contact.department,
            'is_primary': contact.is_primary,
            'notes': contact.notes,
            'appointments': []
        }
        
        # Add appointments for this contact
        for appointment in contact.appointments:
            appointment_data = {
                'id': appointment.id,
                'title': appointment.title,
                'description': appointment.description,
                'appointment_date': appointment.appointment_date.isoformat(),
                'duration_minutes': appointment.duration_minutes,
                'location': appointment.location,
                'appointment_type': appointment.appointment_type,
                'status': appointment.status,
                'notes': appointment.notes
            }
            contact_data['appointments'].append(appointment_data)
        
        customer_data['contacts'].append(contact_data)
    
    return jsonify(customer_data)

# Document management routes
@app.route('/customer/<int:customer_id>/documents')
def customer_documents(customer_id):
    customer = Customer.query.get_or_404(customer_id)
    documents = Document.query.filter_by(customer_id=customer_id).order_by(Document.created_at.desc()).all()
    return render_template('customer_documents.html', customer=customer, documents=documents)

@app.route('/customer/<int:customer_id>/documents/upload', methods=['GET', 'POST'])
def upload_document(customer_id):
    customer = Customer.query.get_or_404(customer_id)
    
    if request.method == 'POST':
        try:
            app.logger.info(f'Upload-Versuch für Kunde {customer_id}')
            
            # Check if file is in request
            if 'file' not in request.files:
                app.logger.error('Keine Datei in der Anfrage')
                return jsonify({'error': 'Keine Datei ausgewählt'}), 400
            
            file = request.files['file']
            description = request.form.get('description', '')
            tags = request.form.get('tags', '')
            upload_method = request.form.get('upload_method', 'upload')
            
            app.logger.info(f'Datei: {file.filename}, Methode: {upload_method}')
            
            if file.filename == '':
                app.logger.error('Leerer Dateiname')
                return jsonify({'error': 'Keine Datei ausgewählt'}), 400
            
            if file and allowed_file(file.filename):
                app.logger.info(f'Datei {file.filename} ist erlaubt')
                # Ensure upload directory exists
                if not os.path.exists(app.config['UPLOAD_FOLDER']):
                    os.makedirs(app.config['UPLOAD_FOLDER'])
                    app.logger.info(f'Upload-Ordner erstellt: {app.config["UPLOAD_FOLDER"]}')
                
                # Generate unique filename
                filename = secure_filename(file.filename)
                unique_filename = f"{uuid.uuid4().hex}_{filename}"
                
                # Save file
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
                app.logger.info(f'Speichere Datei: {file_path}')
                
                # Save file with explicit error handling
                try:
                    file.save(file_path)
                    app.logger.info(f'Datei erfolgreich gespeichert: {file_path}')
                    
                    # Verify file exists and get size
                    if not os.path.exists(file_path):
                        raise Exception(f'Datei wurde nicht gespeichert: {file_path}')
                    
                    file_size = os.path.getsize(file_path)
                    app.logger.info(f'Datei-Größe: {file_size} bytes')
                    
                    # Create document record
                    document = Document(
                        customer_id=customer_id,
                        filename=unique_filename,
                        original_filename=filename,
                        file_size=file_size,
                        mime_type=file.content_type or 'application/octet-stream',
                        upload_method=upload_method,
                        description=description,
                        tags=tags
                    )
                    
                    db.session.add(document)
                    db.session.commit()
                    app.logger.info(f'Dokument in DB gespeichert: {document.id}')
                    
                    # Return success response for AJAX
                    return jsonify({'success': True, 'message': 'Dokument erfolgreich hochgeladen!'})
                    
                except Exception as save_error:
                    app.logger.error(f'Fehler beim Speichern der Datei: {str(save_error)}')
                    return jsonify({'error': f'Fehler beim Speichern der Datei: {str(save_error)}'}), 500
            else:
                app.logger.error(f'Ungültiges Dateiformat: {file.filename}')
                return jsonify({'error': f'Ungültiges Dateiformat. Erlaubte Formate: {", ".join(ALLOWED_EXTENSIONS)}'}), 400
                
        except Exception as e:
            app.logger.error(f'Upload-Fehler: {str(e)}')
            return jsonify({'error': f'Upload-Fehler: {str(e)}'}), 500
    
    return render_template('document_upload.html', customer=customer)

@app.route('/document/<int:document_id>')
def view_document(document_id):
    document = Document.query.get_or_404(document_id)
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], document.filename)
    
    if not os.path.exists(file_path):
        flash('Datei nicht gefunden', 'error')
        return redirect(url_for('customer_documents', customer_id=document.customer_id))
    
    return send_file(file_path, 
                     as_attachment=False,
                     download_name=document.original_filename,
                     mimetype=document.mime_type)

@app.route('/document/<int:document_id>/download')
def download_document(document_id):
    document = Document.query.get_or_404(document_id)
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], document.filename)
    
    if not os.path.exists(file_path):
        flash('Datei nicht gefunden', 'error')
        return redirect(url_for('customer_documents', customer_id=document.customer_id))
    
    return send_file(file_path, 
                     as_attachment=True,
                     download_name=document.original_filename,
                     mimetype=document.mime_type)

@app.route('/document/<int:document_id>/delete', methods=['POST'])
def delete_document(document_id):
    document = Document.query.get_or_404(document_id)
    customer_id = document.customer_id
    
    # Delete file from filesystem
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], document.filename)
    if os.path.exists(file_path):
        os.remove(file_path)
    
    # Delete from database
    db.session.delete(document)
    db.session.commit()
    
    flash('Dokument erfolgreich gelöscht!', 'success')
    return redirect(url_for('customer_documents', customer_id=customer_id))

@app.route('/document/<int:document_id>/edit', methods=['GET', 'POST'])
def edit_document(document_id):
    document = Document.query.get_or_404(document_id)
    
    if request.method == 'POST':
        document.description = request.form.get('description', '')
        document.tags = request.form.get('tags', '')
        document.updated_at = datetime.utcnow()
        
        db.session.commit()
        flash('Dokument erfolgreich aktualisiert!', 'success')
        return redirect(url_for('customer_documents', customer_id=document.customer_id))
    
    return render_template('document_edit.html', document=document)

# PWA Routes
@app.route('/manifest.json')
def manifest():
    return send_file('static/manifest.json', mimetype='application/manifest+json')

@app.route('/sw.js')
def service_worker():
    return send_file('static/sw.js', mimetype='application/javascript')
