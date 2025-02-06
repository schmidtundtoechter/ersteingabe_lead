# Server Script for "Ersteingabe Lead AZ-IT"
# Trigger: Before Save

# Step 1: Create the 'kompletter_name' based on 'vornahme', 'zweiter_vornahme', 'nachnahme'
name_parts = []

if doc.vornahme:
    name_parts.append(doc.vornahme)

if doc.zweiter_vornahme:
    name_parts.append(doc.zweiter_vornahme)

if doc.nachnahme:
    name_parts.append(doc.nachnahme)

# Zusammensetzen der Namensteile mit Leerzeichen
doc.kompletter_name = " ".join(name_parts)

# Step 2: Create new Lead entry
new_lead = frappe.get_doc({
    "doctype": "Lead",
    "status": "Lead",
    "custom_status_intern": "Lead",
    "company_name": doc.hfz,
    "custom_thema": doc.thema,
    "custom_leadquelle": doc.leadquelle,
    "job_title": doc.position,
    "salutation": doc.anrede,
    "first_name": doc.vornahme,
    "middle_name": doc.zweiter_vornahme,
    "last_name": doc.nachnahme,
    "lead_name": doc.kompletter_name,
    "gender": doc.geschlecht,
    "custom_adresse_mutterunternehmen": doc.adresse_mutterunternehmen,
    "custom_kontakt_mutterunternehmen": doc.kontakt_mutterunternehmen,
    "no_of_employees": doc.select_lapl,
    "industry": doc.wirtschaftsbranche,
    "custom_straße": doc.adresse_zeile_1,
    "custom_hausnummer": doc.adresse_zeile_2,
    "custom_ort": doc.ort_wohnort,
    "custom_plz": doc.plz,
    "custom_land": doc.land,
    "address_html": doc.webseite,
    "campaign_name": doc.kampagnenname,
    "language": doc.drucksprache,
    "disabled": doc.deaktiviert,
    "unsubscribed": doc.unsubscribed,
    "blog_subscriber": doc.blog_subscriber,
    "company": "AZ IT-Systems & Consulting GmbH",
    "custom_tel_zentrale": doc.telefon_zentrale,
    "email_id" : doc.email,
    "website" : doc.webseite
    
})

# Speichern des Leads
new_lead.insert(ignore_permissions=True)

# Step 3: Remove automatically generated Contact (if any)
auto_contact = frappe.get_all("Contact", filters={"link_doctype": "Lead", "link_name": new_lead.name})
if auto_contact:
    for contact in auto_contact:
        frappe.delete_doc("Contact", contact.name, ignore_permissions=True)

# Step 4: Create new Contact entry
new_contact = frappe.get_doc({
    "doctype": "Contact",
    "custom_präfix": doc.titel,
    "first_name": doc.vornahme,
    "middle_name": doc.zweiter_vornahme,
    "last_name": doc.nachnahme,
    "salutation": doc.anrede,
    "designation": doc.position,
    "gender": doc.geschlecht,
    "company_name": doc.hfz,
    "status": "Passive",
    "is_primary_contact": doc.ist_hauptkontakt,
    "is_billing_contact": doc.ist_primärer_rechnungskontakt,
    "department": doc.abteilung
})

# Speichern des Kontakts
new_contact.insert(ignore_permissions=True)

# Step 5: Add phone numbers
if doc.telefon:
    new_contact.append("phone_nos", {
        "phone": doc.telefon,
        "is_primary_phone": 1
    })

if doc.telefon_zentrale:
    new_contact.append("phone_nos", {
        "phone": doc.telefon_zentrale
    })

# Speichern des Kontakts nach dem Hinzufügen der Telefonnummern
new_contact.save(ignore_permissions=True)

# Step 6: Add email addresses
if doc.email_ansprechpartner:
    new_contact.append("email_ids", {
        "email_id": doc.email_ansprechpartner,
        "is_primary": 1
    })

if doc.email:
    new_contact.append("email_ids", {
        "email_id": doc.email
    })

# Speichern des Kontakts nach dem Hinzufügen der E-Mail-Adressen
new_contact.save(ignore_permissions=True)

# Step 7: Create new Address entry
new_address = frappe.get_doc({
    "doctype": "Address",
    "address_title": doc.kompletter_name,
    "address_type": "Other",
    "address_line1": doc.adresse_zeile_1,
    "address_line2": doc.adresse_zeile_2,
    "city": doc.ort_wohnort,
    "county": doc.land,
    "pincode": doc.plz,
    "email_id": doc.email,
    "phone": doc.telefon,
    "is_primary_address": doc.ist_hauptkontakt,
    "is_shipping_address": doc.ist_versandanschrift
})

# Link Address to Lead
new_address.append("links", {
    "link_doctype": "Lead",
    "link_name": new_lead.name
})

# Speichern der Adresse
new_address.insert(ignore_permissions=True)

# Step 8: Update Lead with Contact ID
new_lead.custom_aktueller_primärkontakt = new_contact.name
new_lead.save(ignore_permissions=True)

# Step 9: Add the link from Contact to Lead
new_contact.append("links", {
    "link_doctype": "Lead",
    "link_name": new_lead.name,
    "link_title": new_lead.lead_name
})

# Speichern des Kontakts nach Hinzufügen des Links
new_contact.save(ignore_permissions=True)


