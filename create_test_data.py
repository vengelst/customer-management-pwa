#!/usr/bin/env python3
"""
Script to create test data for the customer management system
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import app, db
from models import Customer, Contact, Appointment
from datetime import datetime, timedelta
import random

def create_test_data():
    with app.app_context():
        # Test companies data
        companies = [
            {
                'company_name': 'TechNova Solutions GmbH',
                'industry': 'IT-Dienstleistungen',
                'address': 'Innovationsstraße 12',
                'city': 'München',
                'postal_code': '80333',
                'country': 'Deutschland',
                'website': 'https://technova-solutions.de',
                'category': 'Interesse',
                'notes': 'Großes Interesse an unseren Cloud-Lösungen'
            },
            {
                'company_name': 'Grüne Energie AG',
                'industry': 'Erneuerbare Energien',
                'address': 'Windparkweg 25',
                'city': 'Hamburg',
                'postal_code': '20095',
                'country': 'Deutschland',
                'website': 'https://gruene-energie.de',
                'category': 'Bedarf',
                'notes': 'Benötigt Beratung für Photovoltaik-Anlagen'
            },
            {
                'company_name': 'Maschinenbau Hoffmann',
                'industry': 'Maschinenbau',
                'address': 'Industriestraße 8',
                'city': 'Stuttgart',
                'postal_code': '70173',
                'country': 'Deutschland',
                'website': 'https://hoffmann-maschinenbau.de',
                'category': 'neu',
                'notes': 'Erste Kontaktaufnahme über Messe'
            },
            {
                'company_name': 'Digital Marketing Pro',
                'industry': 'Marketing',
                'address': 'Kreativquartier 15',
                'city': 'Berlin',
                'postal_code': '10115',
                'country': 'Deutschland',
                'website': 'https://digital-marketing-pro.de',
                'category': 'Interesse',
                'notes': 'Interesse an Social Media Tools'
            },
            {
                'company_name': 'Pharma Research Labs',
                'industry': 'Pharmaindustrie',
                'address': 'Forschungsallee 3',
                'city': 'Frankfurt',
                'postal_code': '60311',
                'country': 'Deutschland',
                'website': 'https://pharma-research.de',
                'category': 'Bedarf',
                'notes': 'Dringender Bedarf an Laborautomatisierung'
            },
            {
                'company_name': 'Logistics Express',
                'industry': 'Logistik',
                'address': 'Hafenstraße 44',
                'city': 'Bremen',
                'postal_code': '28195',
                'country': 'Deutschland',
                'website': 'https://logistics-express.de',
                'category': 'kein Bedarf',
                'notes': 'Aktuell keine Investitionen geplant'
            },
            {
                'company_name': 'Bauwerk Konstruktion',
                'industry': 'Baugewerbe',
                'address': 'Bauplatz 7',
                'city': 'Köln',
                'postal_code': '50667',
                'country': 'Deutschland',
                'website': 'https://bauwerk-konstruktion.de',
                'category': 'Interesse',
                'notes': 'Interessiert an BIM-Software'
            },
            {
                'company_name': 'FoodTech Innovations',
                'industry': 'Lebensmitteltechnologie',
                'address': 'Technologiepark 19',
                'city': 'Dortmund',
                'postal_code': '44227',
                'country': 'Deutschland',
                'website': 'https://foodtech-innovations.de',
                'category': 'neu',
                'notes': 'Empfehlung von bestehenden Kunden'
            },
            {
                'company_name': 'Automotive Solutions',
                'industry': 'Automobilindustrie',
                'address': 'Motorstraße 33',
                'city': 'Wolfsburg',
                'postal_code': '38440',
                'country': 'Deutschland',
                'website': 'https://automotive-solutions.de',
                'category': 'Bedarf',
                'notes': 'Sucht Lösungen für Elektromobilität'
            },
            {
                'company_name': 'Finance & Advisory',
                'industry': 'Finanzdienstleistungen',
                'address': 'Bankenplatz 1',
                'city': 'Düsseldorf',
                'postal_code': '40213',
                'country': 'Deutschland',
                'website': 'https://finance-advisory.de',
                'category': 'Interesse',
                'notes': 'Braucht Compliance-Software'
            }
        ]

        # Contacts data for each company
        contacts_data = [
            # TechNova Solutions
            [
                {'first_name': 'Michael', 'last_name': 'Weber', 'title': 'Geschäftsführer', 'email': 'michael.weber@technova-solutions.de', 'phone': '+49 89 12345678', 'mobile': '+49 171 1234567', 'department': 'Geschäftsführung', 'is_primary': True},
                {'first_name': 'Sarah', 'last_name': 'Schmidt', 'title': 'IT-Leiterin', 'email': 'sarah.schmidt@technova-solutions.de', 'phone': '+49 89 12345679', 'mobile': '+49 171 1234568', 'department': 'IT', 'is_primary': False},
                {'first_name': 'Thomas', 'last_name': 'Müller', 'title': 'Projektmanager', 'email': 'thomas.mueller@technova-solutions.de', 'phone': '+49 89 12345680', 'mobile': '+49 171 1234569', 'department': 'Projekte', 'is_primary': False}
            ],
            # Grüne Energie AG
            [
                {'first_name': 'Andrea', 'last_name': 'Hoffmann', 'title': 'Vorstand', 'email': 'andrea.hoffmann@gruene-energie.de', 'phone': '+49 40 23456789', 'mobile': '+49 172 2345678', 'department': 'Vorstand', 'is_primary': True},
                {'first_name': 'Robert', 'last_name': 'Klein', 'title': 'Technischer Leiter', 'email': 'robert.klein@gruene-energie.de', 'phone': '+49 40 23456790', 'mobile': '+49 172 2345679', 'department': 'Technik', 'is_primary': False}
            ],
            # Maschinenbau Hoffmann
            [
                {'first_name': 'Klaus', 'last_name': 'Hoffmann', 'title': 'Inhaber', 'email': 'klaus.hoffmann@hoffmann-maschinenbau.de', 'phone': '+49 711 34567890', 'mobile': '+49 173 3456789', 'department': 'Geschäftsführung', 'is_primary': True},
                {'first_name': 'Maria', 'last_name': 'Becker', 'title': 'Einkaufsleiterin', 'email': 'maria.becker@hoffmann-maschinenbau.de', 'phone': '+49 711 34567891', 'mobile': '+49 173 3456790', 'department': 'Einkauf', 'is_primary': False},
                {'first_name': 'Stefan', 'last_name': 'Wolf', 'title': 'Produktionsleiter', 'email': 'stefan.wolf@hoffmann-maschinenbau.de', 'phone': '+49 711 34567892', 'mobile': '+49 173 3456791', 'department': 'Produktion', 'is_primary': False}
            ],
            # Digital Marketing Pro
            [
                {'first_name': 'Lisa', 'last_name': 'Braun', 'title': 'Creative Director', 'email': 'lisa.braun@digital-marketing-pro.de', 'phone': '+49 30 45678901', 'mobile': '+49 174 4567890', 'department': 'Creative', 'is_primary': True},
                {'first_name': 'David', 'last_name': 'Wagner', 'title': 'Account Manager', 'email': 'david.wagner@digital-marketing-pro.de', 'phone': '+49 30 45678902', 'mobile': '+49 174 4567891', 'department': 'Account Management', 'is_primary': False}
            ],
            # Pharma Research Labs
            [
                {'first_name': 'Dr. Anna', 'last_name': 'Fischer', 'title': 'Forschungsleiterin', 'email': 'anna.fischer@pharma-research.de', 'phone': '+49 69 56789012', 'mobile': '+49 175 5678901', 'department': 'Forschung', 'is_primary': True},
                {'first_name': 'Martin', 'last_name': 'Richter', 'title': 'Laborleiter', 'email': 'martin.richter@pharma-research.de', 'phone': '+49 69 56789013', 'mobile': '+49 175 5678902', 'department': 'Labor', 'is_primary': False},
                {'first_name': 'Julia', 'last_name': 'Kraus', 'title': 'Qualitätsmanagerin', 'email': 'julia.kraus@pharma-research.de', 'phone': '+49 69 56789014', 'mobile': '+49 175 5678903', 'department': 'Qualität', 'is_primary': False}
            ],
            # Logistics Express
            [
                {'first_name': 'Frank', 'last_name': 'Neumann', 'title': 'Geschäftsführer', 'email': 'frank.neumann@logistics-express.de', 'phone': '+49 421 67890123', 'mobile': '+49 176 6789012', 'department': 'Geschäftsführung', 'is_primary': True},
                {'first_name': 'Petra', 'last_name': 'Lange', 'title': 'Disponentin', 'email': 'petra.lange@logistics-express.de', 'phone': '+49 421 67890124', 'mobile': '+49 176 6789013', 'department': 'Disposition', 'is_primary': False}
            ],
            # Bauwerk Konstruktion
            [
                {'first_name': 'Jürgen', 'last_name': 'Zimmermann', 'title': 'Bauleiter', 'email': 'juergen.zimmermann@bauwerk-konstruktion.de', 'phone': '+49 221 78901234', 'mobile': '+49 177 7890123', 'department': 'Bauleitung', 'is_primary': True},
                {'first_name': 'Sabine', 'last_name': 'Hartmann', 'title': 'Architektin', 'email': 'sabine.hartmann@bauwerk-konstruktion.de', 'phone': '+49 221 78901235', 'mobile': '+49 177 7890124', 'department': 'Architektur', 'is_primary': False}
            ],
            # FoodTech Innovations
            [
                {'first_name': 'Oliver', 'last_name': 'Fuchs', 'title': 'CEO', 'email': 'oliver.fuchs@foodtech-innovations.de', 'phone': '+49 231 89012345', 'mobile': '+49 178 8901234', 'department': 'Geschäftsführung', 'is_primary': True},
                {'first_name': 'Nicole', 'last_name': 'Schulz', 'title': 'Entwicklungsleiterin', 'email': 'nicole.schulz@foodtech-innovations.de', 'phone': '+49 231 89012346', 'mobile': '+49 178 8901235', 'department': 'Entwicklung', 'is_primary': False},
                {'first_name': 'Markus', 'last_name': 'Vogel', 'title': 'Vertriebsleiter', 'email': 'markus.vogel@foodtech-innovations.de', 'phone': '+49 231 89012347', 'mobile': '+49 178 8901236', 'department': 'Vertrieb', 'is_primary': False}
            ],
            # Automotive Solutions
            [
                {'first_name': 'Christine', 'last_name': 'Lorenz', 'title': 'Geschäftsführerin', 'email': 'christine.lorenz@automotive-solutions.de', 'phone': '+49 5361 90123456', 'mobile': '+49 179 9012345', 'department': 'Geschäftsführung', 'is_primary': True},
                {'first_name': 'Alexander', 'last_name': 'Weiß', 'title': 'Entwicklungsleiter', 'email': 'alexander.weiss@automotive-solutions.de', 'phone': '+49 5361 90123457', 'mobile': '+49 179 9012346', 'department': 'Entwicklung', 'is_primary': False}
            ],
            # Finance & Advisory
            [
                {'first_name': 'Dr. Matthias', 'last_name': 'Lehmann', 'title': 'Partner', 'email': 'matthias.lehmann@finance-advisory.de', 'phone': '+49 211 01234567', 'mobile': '+49 180 0123456', 'department': 'Partnership', 'is_primary': True},
                {'first_name': 'Eva', 'last_name': 'Sommer', 'title': 'Beraterin', 'email': 'eva.sommer@finance-advisory.de', 'phone': '+49 211 01234568', 'mobile': '+49 180 0123457', 'department': 'Beratung', 'is_primary': False},
                {'first_name': 'Benjamin', 'last_name': 'Kaiser', 'title': 'Analyst', 'email': 'benjamin.kaiser@finance-advisory.de', 'phone': '+49 211 01234569', 'mobile': '+49 180 0123458', 'department': 'Analyse', 'is_primary': False}
            ]
        ]

        # Appointment titles for different types
        appointment_titles = [
            'Erstberatung', 'Produktpräsentation', 'Vertragsverhandlung', 'Projektstatus-Meeting',
            'Technische Besprechung', 'Angebotspräsentation', 'Nachfassgespräch', 'Kundenfeedback',
            'Schulungsplanung', 'Wartungstermin', 'Strategiemeeting', 'Budgetplanung',
            'Bedarfsanalyse', 'Systemdemonstration', 'Vertragsabschluss', 'Projektstart',
            'Zwischenpräsentation', 'Abnahmetest', 'Go-Live Vorbereitung', 'Projektabschluss'
        ]

        appointment_types = ['meeting', 'call', 'email', 'visit']
        appointment_statuses = ['scheduled', 'completed', 'cancelled']

        print("Creating test customers...")
        
        # Create customers
        for i, company_data in enumerate(companies):
            customer = Customer(**company_data)
            db.session.add(customer)
            db.session.flush()  # Get the ID
            
            print(f"Created customer: {customer.company_name}")
            
            # Create contacts for this customer
            for j, contact_data in enumerate(contacts_data[i]):
                contact = Contact(customer_id=customer.id, **contact_data)
                db.session.add(contact)
                db.session.flush()  # Get the ID
                
                print(f"  Created contact: {contact.full_name}")
                
                # Create appointments for this contact
                for k in range(4):  # 4 appointments per contact
                    if k < 3:  # 3 past appointments
                        appointment_date = datetime.now() - timedelta(days=random.randint(1, 90))
                        status = random.choice(['completed', 'cancelled'])
                    else:  # 1 future appointment
                        appointment_date = datetime.now() + timedelta(days=random.randint(1, 60))
                        status = 'scheduled'
                    
                    appointment = Appointment(
                        contact_id=contact.id,
                        title=random.choice(appointment_titles),
                        description=f"Besprechung mit {contact.full_name} von {customer.company_name}",
                        appointment_date=appointment_date,
                        duration_minutes=random.choice([30, 60, 90, 120]),
                        location=random.choice(['Büro', 'Online', 'Telefon', 'Kunde vor Ort']),
                        appointment_type=random.choice(appointment_types),
                        status=status,
                        notes=f"Wichtiger Termin bezüglich {customer.category}"
                    )
                    db.session.add(appointment)
                    
                    print(f"    Created appointment: {appointment.title} ({appointment.appointment_date.strftime('%d.%m.%Y %H:%M')})")
        
        db.session.commit()
        print(f"\nTest data created successfully!")
        print(f"Created {len(companies)} customers with contacts and appointments")

if __name__ == '__main__':
    create_test_data()