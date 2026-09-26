"""Static site generator for the stationery site.
Run:  python _build/build.py      (from the project folder)
All brand + contact placeholders live in CONFIG below. Edit, re-run, done.
Output is plain static HTML in the project root (no runtime dependencies).
"""
import json
import os
import urllib.parse
from html import escape as esc
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ---------------------------------------------------------------- CONFIG ---
CONFIG = dict(
    brand="Inkwell & Co.",
    brand_html='Inkwell <span class="logo-amp">&amp;</span> Co.',
    city="Dubai",
    country="UAE",
    kind="wholesale distributor",
    email="sales@inkwellco.example",
    phone="+971 4 000 0000",
    phone_tel="+97140000000",
    wa_number="971500000000",
    wa_display="+971 50 000 0000",
    address="Warehouse 12, Al Quoz Industrial Area 3, Dubai, UAE",
    hours=[("Saturday – Thursday", "8:30 am – 6:00 pm"), ("Friday", "Closed")],
    social=[("Instagram", "#"), ("LinkedIn", "#"), ("Facebook", "#")],
    years="12+", products="2,500+", clients="850+", coverage="UAE-wide",
)
C = CONFIG
WA_BASE = "https://wa.me/%s?text=" % C["wa_number"]
WA_HELLO = WA_BASE + urllib.parse.quote("Hi %s, I would like to enquire about your stationery." % C["brand"])

ICONS = {
    "award": '<circle cx="12" cy="8" r="6"/><path d="M15.5 13.5 17 22l-5-3-5 3 1.5-8.5"/>',
    "tag": '<path d="M20.6 13.4 13.4 20.6a2 2 0 0 1-2.8 0L2 12V2h10l8.6 8.6a2 2 0 0 1 0 2.8z"/><circle cx="7" cy="7" r="1.5"/>',
    "truck": '<path d="M1 3h15v13H1z"/><path d="M16 8h4l3 3v5h-7V8z"/><circle cx="5.5" cy="18.5" r="2.5"/><circle cx="18.5" cy="18.5" r="2.5"/>',
    "pen": '<path d="M12 20h9"/><path d="M16.5 3.5a2.1 2.1 0 0 1 3 3L7 19l-4 1 1-4z"/>',
    "layers": '<path d="m12 2 10 5-10 5L2 7z"/><path d="m2 17 10 5 10-5"/><path d="m2 12 10 5 10-5"/>',
    "book": '<path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"/><path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"/>',
    "briefcase": '<rect x="2" y="7" width="20" height="14" rx="2"/><path d="M16 21V5a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v16"/>',
    "landmark": '<path d="M3 21h18M5 21V10m4 11V10m6 11V10m4 11V10M2 10l10-7 10 7z"/>',
    "coffee": '<path d="M18 8h1a4 4 0 0 1 0 8h-1"/><path d="M2 8h16v9a4 4 0 0 1-4 4H6a4 4 0 0 1-4-4z"/><path d="M6 1v3M10 1v3M14 1v3"/>',
    "store": '<path d="M3 9l1-5h16l1 5"/><path d="M3 9a3 3 0 0 0 6 0 3 3 0 0 0 6 0 3 3 0 0 0 6 0"/><path d="M5 12v9h14v-9"/>',
    "phone": '<path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1 1 .4 1.9.7 2.8a2 2 0 0 1-.5 2.1L8.1 9.9a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.4c.9.3 1.8.6 2.8.7a2 2 0 0 1 1.7 2z"/>',
    "mail": '<rect x="2" y="4" width="20" height="16" rx="2"/><path d="m22 7-10 6L2 7"/>',
    "pin": '<path d="M21 10c0 7-9 13-9 13S3 17 3 10a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/>',
    "clock": '<circle cx="12" cy="12" r="10"/><path d="M12 6v6l4 2"/>',
    "download": '<path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><path d="m7 10 5 5 5-5"/><path d="M12 15V3"/>',
    "arrow": '<path d="M5 12h14M13 5l7 7-7 7"/>',
    "check": '<path d="M20 6 9 17l-5-5"/>',
    "menu": '<path d="M3 6h18M3 12h18M3 18h18"/>',
    "close": '<path d="M18 6 6 18M6 6l12 12"/>',
    "chevron": '<path d="m6 9 6 6 6-6"/>',
    "upload": '<path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><path d="m17 8-5-5-5 5"/><path d="M12 3v12"/>',
    "eye": '<path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8S1 12 1 12z"/><circle cx="12" cy="12" r="3"/>',
    "package": '<path d="M21 8 12 3 3 8v8l9 5 9-5z"/><path d="M3.3 7 12 12l8.7-5M12 22V12"/>',
    "palette": '<circle cx="13.5" cy="6.5" r="1.5"/><circle cx="17.5" cy="10.5" r="1.5"/><circle cx="8.5" cy="7.5" r="1.5"/><circle cx="6.5" cy="12.5" r="1.5"/><path d="M12 2a10 10 0 1 0 0 20c1.1 0 2-.9 2-2 0-.5-.2-1-.5-1.3-.3-.4-.5-.8-.5-1.3 0-1.1.9-2 2-2h2.4a4.6 4.6 0 0 0 4.6-4.6C22 6 17.5 2 12 2z"/>',
    "star": '<path d="m12 2 3.1 6.3 6.9 1-5 4.9 1.2 6.8L12 17.8 5.8 21l1.2-6.8-5-4.9 6.9-1z"/>',
    "shield": '<path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/><path d="m9 12 2 2 4-4"/>',
    "instagram": '<rect x="2" y="2" width="20" height="20" rx="5"/><circle cx="12" cy="12" r="4"/><circle cx="17.5" cy="6.5" r=".8"/>',
    "linkedin": '<path d="M16 8a6 6 0 0 1 6 6v7h-4v-7a2 2 0 0 0-4 0v7h-4v-7a6 6 0 0 1 6-6z"/><rect x="2" y="9" width="4" height="12"/><circle cx="4" cy="4" r="2"/>',
    "facebook": '<path d="M18 2h-3a5 5 0 0 0-5 5v3H7v4h3v8h4v-8h3l1-4h-4V7a1 1 0 0 1 1-1h3z"/>',
}
WA_PATH = ('<path d="M12.04 2a9.9 9.9 0 0 0-8.5 14.9L2 22l5.2-1.4A9.9 9.9 0 1 0 12.04 2zm0 1.8a8.1 8.1 0 1 1-4.3 15l-.3-.2-3 .8.8-2.9-.2-.3a8.1 8.1 0 0 1 7-12.4zM8.7 7.6c-.2 0-.5.1-.7.4-.3.3-1 1-1 2.4s1 2.8 1.2 3c.1.2 2 3.1 4.900 4.300 2.400 1 2.900.8 3.400.7.500-.1 1.700-.7 1.900-1.400.2-.7.2-1.200.2-1.400-.1-.1-.3-.2-.6-.3l-1.900-.9c-.3-.1-.5-.1-.7.1l-.9 1.100c-.2.200-.3.200-.6.100-.9-.4-1.700-.9-2.500-1.700-.6-.6-1.100-1.400-1.400-2-.100-.3 0-.4.200-.6l.4-.5.3-.5v-.5l-.9-2.100c-.2-.5-.4-.5-.6-.5z"/>')


def icon(name, cls=""):
    return '<svg class="icon %s" viewBox="0 0 24 24" aria-hidden="true" focusable="false">%s</svg>' % (cls, ICONS[name])


def wa_icon(cls="icon--fill"):
    return '<svg class="icon %s" viewBox="0 0 24 24" aria-hidden="true" focusable="false">%s</svg>' % (cls, WA_PATH)


LOGO_MARK = ('<svg class="logo-mark" viewBox="0 0 40 40" aria-hidden="true"><rect x="2" y="2" width="36" height="36" rx="10" fill="#0F1B3D"/>'
             '<path d="M20 7.5 28 20l-8 12.500L12 20z" fill="#FFD84A"/><circle cx="20" cy="18.500" r="2.600" fill="#0F1B3D"/><path d="M20 21v8" stroke="#0F1B3D" stroke-width="2"/></svg>')
LOGO_MARK_LIGHT = LOGO_MARK.replace('fill="#0F1B3D"/>', 'fill="#FBF7EF"/>', 1)

# ------------------------------------------------------------------ DATA ---
_dim_cache = {}


def img(name, alt, cls="", eager=False, sizes=None, pos=None):
    path = os.path.join(ROOT, "assets", "img", name + ".jpg")
    if name not in _dim_cache:
        with Image.open(path) as im:
            _dim_cache[name] = im.size
    w, h = _dim_cache[name]
    style = ' style="object-position:%s"' % pos if pos else ""
    return '<img src="assets/img/%s.jpg" alt="%s" width="%d" height="%d"%s%s%s%s>' % (
        name, esc(alt, True), w, h, ' class="%s"' % cls if cls else "",
        "" if eager else ' loading="lazy" decoding="async"', ' sizes="%s"' % sizes if sizes else "", style)


CATS = [
    dict(slug="office-products", name="Office Products", tag="var(--c-office)", accent="#ffd84a", img="desk2",
         alt="Desk with notebooks, pens and everyday office stationery",
         tagline="Everything that lives on a working desk.",
         intro="From the pen in your hand to the cabinet that keeps every record safe, our office range covers the daily essentials that keep teams productive. Stocked in depth and ready for bulk orders.",
         short="Paper, pens, organisers, labels, sticky notes and the small things that keep a desk running.",
         subs=[
             ("Paper Products", "Copier paper, notebooks, pads and forms in the sizes and weights offices reorder every month.", "notebook", "50% 50%"),
             ("Desktop Organizers", "Trays, pen pots and mesh sets that turn a cluttered desk into a calm one.", "desk", "30% 60%"),
             ("Writing Instruments", "Ballpoints, gel pens, markers and highlighters for offices, classrooms and counters.", "pencils", "50% 40%"),
             ("Stamps & Ink", "Self-inking stamps, dater stamps and refill ink for approvals, receipts and mailrooms.", "desk2", "80% 30%"),
             ("Packing Supplies", "Tape, bubble wrap, mailers and cartons for dispatch teams that ship every day.", "warehouse", "50% 50%"),
             ("Labels", "Address, barcode and file labels in sheets and rolls, plain or printed.", "sticky-wall", "20% 60%"),
             ("Sticky Notes & Flags", "Neon pads, page flags and index tabs in every size, sold by the carton.", "sticky", "50% 50%"),
             ("ID Holders & Lanyards", "Badge holders and lanyards for staff, visitors and events, printable with your logo.", "team", "50% 40%"),
             ("Key Cabinets", "Lockable steel key boxes for reception desks, facilities teams and property offices.", "cabinet", "70% 50%"),
             ("Filing Cabinets", "Steel and lockable cabinets in two, three and four drawers, built for heavy daily use.", "cabinet", "20% 40%"),
         ]),
    dict(slug="files-folders", name="Files & Folders", tag="var(--c-files)", accent="#ff7a66", img="binders",
         alt="Rows of colourful ring binders on office shelves",
         tagline="Organised paperwork, made to last.",
         intro="Ring binders, box files and organisers that hold up to years of handling, in classic colours or custom-printed with your company branding.",
         short="Ring binders, box files, organisers and custom-branded files for every archive.",
         subs=[
             ("Ring Binders", "Lever-arch and D-ring binders in PVC and board, A4, A5 and foolscap.", "binder-open", "50% 50%"),
             ("Box Files", "Sturdy box files with metal-edged spines for archives and project paperwork.", "binders", "30% 50%"),
             ("Document Organizers", "Expanding files, folders and document cases that travel with your paperwork.", "folders", "50% 50%"),
             ("Filing Accessories", "Dividers, punched pockets, spine labels and reinforcement rings that complete a filing system.", "sticky-wall", "50% 30%"),
             ("Customised Files", "Files, binders and folders printed with your logo, colours and details. Minimum order applies.", "binders", "80% 60%"),
         ]),
    dict(slug="office-equipment", name="Office Equipment", tag="var(--c-equip)", accent="#5aa9ff", img="office",
         alt="Modern office desk with chair and computer",
         tagline="The machines behind a tidy, efficient office.",
         intro="Laminators, shredders and computer accessories chosen for reliability. Easy to run, easy to service and supplied with the consumables they need.",
         short="Laminators, shredders and computer accessories that keep the office moving.",
         subs=[
             ("Laminating Machines & Pouches", "Hot and cold laminators for A4 to A3, with pouches in matching sizes and thicknesses.", "office", "50% 30%"),
             ("Shredders", "Strip-cut and cross-cut shredders from personal units to heavy-duty office machines.", "cabinet", "60% 60%"),
             ("Computer Accessories", "Keyboards, mice, cables, stands and storage for every workstation.", "desk2", "70% 40%"),
         ]),
    dict(slug="boards-display", name="Boards & Display", tag="var(--c-boards)", accent="#3fc79a", img="whiteboard",
         alt="Person writing on a whiteboard with an orange marker",
         tagline="Say it, pin it, present it.",
         intro="Whiteboards, notice boards and display stands for meeting rooms, classrooms, reception areas and retail counters.",
         short="Whiteboards, notice boards, flip charts, easels and display holders.",
         subs=[
             ("Whiteboards", "Magnetic and non-magnetic boards in aluminium frames, wall-mounted or on stands.", "whiteboard", "50% 40%"),
             ("Cork & Felt Boards", "Pin-friendly cork and coloured felt boards for offices and classrooms.", "cork", "50% 50%"),
             ("Notice Boards", "Lockable and open notice boards for corridors, receptions and schools.", "sticky", "60% 50%"),
             ("Flip Charts & Easels", "Tripod easels and flip chart pads for workshops, training and presentations.", "team", "50% 50%"),
             ("Brochure & Sign Holders", "Acrylic and metal holders for brochures, price lists and door signs.", "clipboard", "30% 50%"),
             ("Magnets", "Strong board magnets in assorted shapes and colours.", "sticky-wall", "80% 40%"),
         ]),
    dict(slug="school-art-craft", name="School, Art & Craft", tag="var(--c-school)", accent="#b58cff", img="school",
         alt="Stationery supplies arranged on a green surface",
         tagline="Ready for the bell.",
         intro="Clipboards, drawing cases and book covers for schools and learners. Durable, colourful and priced for bulk school orders.",
         short="Clipboards, drawing and storage cases and book covers for schools.",
         subs=[
             ("Clipboards", "Hardboard and acrylic clipboards in A4 and foolscap for classrooms and site teams.", "clipboard", "50% 50%"),
             ("Drawing & Storage Cases", "Carry cases and storage boxes for art supplies, drawings and craft kits.", "bucket", "50% 50%"),
             ("Book Covers", "Clear and coloured book covers that protect textbooks all year.", "pencils-white", "50% 50%"),
         ]),
]
for c in CATS:
    for i, s in enumerate(c["subs"]):
        c["subs"][i] = dict(name=s[0], desc=s[1], img=s[2], pos=s[3], slug=s[0].lower().replace(" & ", "-").replace(" ", "-").replace(",", ""))

PRODUCTS = [
    dict(slug="ring-binder", file="product-ring-binder.html", name="A4 PVC Ring Binder, 2 D-Ring", short="A4 PVC Ring Binder", cat=1,
         sku="IW-FF-204", img="binder-open", badge="Best seller",
         title="A4 PVC Ring Binder 2 D-Ring in Bulk | Inkwell & Co.",
         meta="Durable A4 PVC ring binders with 2 D-ring mechanism in five colours. Bulk pricing and custom logo printing available. Request a quote.",
         desc="A workhorse binder for offices and schools. Rigid board wrapped in wipe-clean PVC, a smooth-action 2 D-ring mechanism that holds up to 350 sheets, and a spine label pocket for quick retrieval. Available plain or printed with your company logo.",
         gallery=[("binder-open", "Open ring binder holding a notebook and paper"), ("binders", "Rows of ring binders on an office shelf"), ("folders", "Stack of thick folders on a white surface")],
         options=[("colour", "Colour", [("Navy", "#1f3a8a"), ("Red", "#e5484d"), ("Black", "#1a1a1a"), ("Green", "#1f9d74"), ("Yellow", "#ffd84a")]),
                  ("size", "Size", ["A4", "A5", "Foolscap"]),
                  ("pack", "Pack quantity", ["Box of 12", "Box of 24", "Carton of 96"])],
         specs=[("Material", "1.8 mm rigid board, PVC covered"), ("Mechanism", "2 D-ring, 25 mm or 40 mm capacity"), ("Capacity", "Up to 350 sheets (80 gsm)"), ("Spine", "Label pocket, 50 mm"), ("Finish", "Matt, wipe-clean"), ("Customisation", "Logo print, foil or embossing, minimum 100 pcs"), ("Origin", "Placeholder: add country of origin")],
         features=["Wipe-clean PVC cover", "Smooth D-ring mechanism", "Reinforced spine and edges", "Label pocket on spine", "Custom printing available"],
         related=["magnetic-whiteboard", "sticky-notes"]),
    dict(slug="magnetic-whiteboard", file="product-magnetic-whiteboard.html", name="Magnetic Whiteboard, Aluminium Frame", short="Magnetic Whiteboard", cat=3,
         sku="IW-BD-118", img="whiteboard", badge="Popular for schools",
         title="Magnetic Whiteboard with Aluminium Frame | Inkwell & Co.",
         meta="Magnetic whiteboards with slim aluminium frames in sizes from 60x90 cm to 120x180 cm. Bulk supply for offices and schools. Request a quote.",
         desc="A smooth, ghost-resistant magnetic surface in a slim aluminium frame. Wall-mount fixings and a marker tray are included. Sized for meeting rooms, classrooms and training centres.",
         gallery=[("whiteboard", "Person writing on a whiteboard with an orange marker"), ("cork", "Notes pinned on a board"), ("team", "Team using pens around a meeting table")],
         options=[("frame", "Frame", [("Silver", "#c3c8d4"), ("Black", "#1a1a1a"), ("White", "#f4f4f4")]),
                  ("size", "Size", ["60 x 90 cm", "90 x 120 cm", "120 x 180 cm"]),
                  ("pack", "Pack quantity", ["Single", "Carton of 4"])],
         specs=[("Surface", "Magnetic, ghost-resistant enamel finish"), ("Frame", "Slim anodised aluminium"), ("Includes", "Marker tray, wall fixings, corner caps"), ("Mounting", "Landscape or portrait"), ("Thickness", "17 mm"), ("Warranty", "Placeholder: add warranty terms")],
         features=["Magnetic surface", "Easy-clean, low-ghosting finish", "Includes marker tray", "Wall-mount fixings supplied", "Bulk school and office pricing"],
         related=["ring-binder", "sticky-notes"]),
    dict(slug="sticky-notes", file="product-sticky-notes.html", name="Sticky Notes, Neon Assorted", short="Neon Sticky Notes", cat=0,
         sku="IW-OP-076", img="sticky", badge="New",
         title="Neon Sticky Notes Assorted, Wholesale | Inkwell & Co.",
         meta="Repositionable neon sticky notes in three sizes and assorted colours, sold by the box or carton. Wholesale pricing. Request a quote.",
         desc="Bright, repositionable notes with a strong, clean-release adhesive. Sold in assorted neon packs for offices, classrooms and creative teams, by the pack, box or carton.",
         gallery=[("sticky", "Colourful sticky notes pinned to a board"), ("sticky-wall", "Two blank neon sticky notes on a white wall"), ("notebook", "Purple notebook, pencil and gold clips on white")],
         options=[("colour", "Colour", [("Neon assorted", "#ff7ac6"), ("Canary yellow", "#ffe94a"), ("Pastel mix", "#b9e4d0")]),
                  ("size", "Size", ["76 x 76 mm", "76 x 127 mm", "51 x 38 mm"]),
                  ("pack", "Pack quantity", ["Pack of 12 pads", "Box of 48 pads", "Carton of 240 pads"])],
         specs=[("Sheets per pad", "100"), ("Adhesive", "Repositionable, residue-free"), ("Paper", "70 gsm"), ("Colours", "Neon assorted, canary, pastel"), ("Customisation", "Printed pads, minimum 500 pads"), ("Origin", "Placeholder: add country of origin")],
         features=["Strong, clean-release adhesive", "Bright neon colours", "Three sizes", "Printed pads for promotions", "Carton pricing for resellers"],
         related=["ring-binder", "magnetic-whiteboard"]),
]

FAQS = [
    ("Do you sell to individuals or only to businesses?", "We focus on bulk and repeat supply for offices, schools, government departments, retailers and resellers. Small trial orders are welcome. Send us a request and we will tell you the best way to buy."),
    ("How do I get a price?", "Use the Request a Quote form, WhatsApp us, call or email. Tell us the products and quantities, and we reply with a written quotation, usually within one working day."),
    ("What is the minimum order quantity?", "Standard catalogue items have no strict minimum, but bulk pricing starts at carton quantities. Customised and printed items have a minimum order, typically from 100 pieces for files and binders."),
    ("Can you print our logo on files, binders and folders?", "Yes. We offer screen print, foil stamping, embossing and digital print on files, binders and folders. Send your artwork, approve a proof, and we produce and deliver. See our Customisation page for the full process."),
    ("How long does delivery take?", "In-stock items are typically dispatched within 1 to 2 working days inside the UAE. Customised orders usually take 10 to 15 working days from artwork approval. Placeholder: confirm your real lead times."),
    ("Do you deliver outside the city?", "Yes, we deliver across the UAE. Placeholder: list your delivery coverage, free-delivery threshold and any export options."),
    ("What payment terms do you offer?", "We accept bank transfer and card payments. Approved corporate, school and government accounts can apply for credit terms. Placeholder: confirm your real terms."),
    ("Can I get your product catalogue?", "Absolutely. You can download the full catalogue as a PDF from our Catalogue page, or ask us to send you a printed copy."),
    ("Do you supply tenders and government orders?", "Yes. We are experienced with tender documentation, supplier registration and scheduled deliveries for government offices. Placeholder: add your vendor registrations."),
]

TESTIMONIALS = [
    ("Our purchasing runs on repeat orders and Inkwell never misses a delivery. The custom-printed binders for our clients were spot on.", "Placeholder Name", "Procurement Manager, Corporate client", "var(--c-office)", 5),
    ("Back-to-school used to be a scramble. Now we send one list and the whole order arrives labelled by grade. Genuinely saves our admin team days.", "Placeholder Name", "Head of Administration, School", "var(--c-school)", 5),
    ("Competitive on bulk pricing, quick with quotes, and the quality is consistent. That is all a reseller needs from a supplier.", "Placeholder Name", "Owner, Stationery retailer", "var(--c-boards)", 5),
    ("Clear paperwork, on-time delivery and the right documents for our tender file. Easy to work with.", "Placeholder Name", "Operations Officer, Government office", "var(--c-equip)", 5),
    ("We ordered lanyards and ID holders with our logo for a conference. Proof in a day, delivered in ten. Excellent.", "Placeholder Name", "Events Coordinator, Hospitality group", "var(--c-files)", 5),
    ("Wide range means one supplier instead of five. Their WhatsApp support is quick and actually helpful.", "Placeholder Name", "Office Manager, Consultancy", "var(--c-office)", 4),
]

NAV = [("Customisation", "customisation.html"), ("About", "about.html"), ("Catalogue", "catalogue.html"), ("FAQs", "faqs.html"), ("Contact", "contact.html")]


# ------------------------------------------------------------- TEMPLATES ---
def wa_link(msg):
    return WA_BASE + urllib.parse.quote(msg)


def quote_link(product=None):
    return "contact.html" + ("?product=" + urllib.parse.quote(product) if product else "") + "#quote"


def cat_page(cat):
    return cat["slug"] + ".html"


def header(current):
    mega = ""
    drawer_cats = ""
    for c in CATS:
        items = "".join('<li><a href="%s#%s">%s</a></li>' % (cat_page(c), s["slug"], esc(s["name"])) for s in c["subs"])
        mega += '<div class="mega-col" style="--tag:%s"><h3><a href="%s">%s</a></h3><ul>%s</ul></div>' % (c["tag"], cat_page(c), esc(c["name"]), items)
        drawer_cats += '<li><a class="drawer-sub" href="%s">%s (all)</a></li>' % (cat_page(c), esc(c["name"]))
        drawer_cats += "".join('<li><a href="%s#%s">%s</a></li>' % (cat_page(c), s["slug"], esc(s["name"])) for s in c["subs"])
    nav_items = ""
    for label, href in NAV:
        cur = ' aria-current="page"' if current == href else ""
        nav_items += '<li class="nav-item"><a class="nav-link" href="%s"%s>%s</a></li>' % (href, cur, label)
    prod_cur = ' aria-current="page"' if current in ("products.html",) or current in [cat_page(c) for c in CATS] or current.startswith("product-") else ""
    drawer_links = "".join('<a href="%s">%s</a>' % (h, l) for l, h in NAV)
    hours = "%s: %s" % (C["hours"][0][0], C["hours"][0][1])
    return f'''<a class="skip-link" href="#main">Skip to content</a>
<div class="topbar"><div class="container">
  <div class="topbar-group"><a href="tel:{C['phone_tel']}">{icon('phone')} {C['phone']}</a><a href="mailto:{C['email']}">{icon('mail')} {C['email']}</a></div>
  <div class="topbar-group topbar-group--right"><span>{hours}</span><a href="{WA_HELLO}" target="_blank" rel="noopener">{wa_icon()} WhatsApp us</a></div>
</div></div>
<header class="site-header"><div class="container header-inner">
  <a class="logo" href="index.html" aria-label="{esc(C['brand'])} home">{LOGO_MARK}<span>{C['brand_html']}</span></a>
  <nav class="nav" aria-label="Main">
    <ul class="nav-list">
      <li class="nav-item nav-item--mega"><button class="nav-link" type="button" aria-expanded="false" aria-haspopup="true"{prod_cur}>Products {icon('chevron')}</button>
        <div class="mega">{mega}</div></li>
      {nav_items}
    </ul>
  </nav>
  <div class="header-cta"><a class="btn btn--primary btn--small" href="{quote_link()}">Request a Quote</a>
    <button class="nav-toggle" type="button" aria-label="Open menu" aria-expanded="false" aria-controls="drawer">{icon('menu')}</button></div>
</div></header>
<div class="drawer-scrim" data-drawer-close></div>
<aside class="mobile-drawer" id="drawer" aria-label="Menu">
  <button class="nav-toggle drawer-close" type="button" aria-label="Close menu" data-drawer-close>{icon('close')}</button>
  <a href="index.html">Home</a>
  <details><summary>Products</summary><ul><li><a class="drawer-sub" href="products.html">All products</a></li>{drawer_cats}</ul></details>
  {drawer_links}
  <div class="drawer-cta"><a class="btn btn--primary" href="{quote_link()}">Request a Quote</a>
    <a class="btn btn--wa" href="{WA_HELLO}" target="_blank" rel="noopener">{wa_icon()} WhatsApp</a>
    <a class="btn" href="tel:{C['phone_tel']}">{icon('phone')} Call us</a></div>
</aside>'''


def footer():
    cats = "".join('<li><a href="%s">%s</a></li>' % (cat_page(c), esc(c["name"])) for c in CATS)
    soc = "".join('<li><a href="%s" aria-label="%s">%s</a></li>' % (h, n, icon(n.lower())) for n, h in C["social"])
    return f'''<footer class="site-footer"><div class="container">
  <div class="footer-top">
    <div class="footer-brand"><a class="logo logo--light" href="index.html">{LOGO_MARK_LIGHT}<span>{C['brand_html']}</span></a>
      <p>Office and school stationery for businesses, schools and resellers in {C['country']}. Quality supplies, sharp bulk pricing and fast delivery.</p>
      <ul class="socials">{soc}</ul></div>
    <div class="footer-col"><h3>Products</h3><ul>{cats}</ul></div>
    <div class="footer-col"><h3>Company</h3><ul><li><a href="about.html">About us</a></li><li><a href="customisation.html">Customisation</a></li><li><a href="catalogue.html">Catalogue (PDF)</a></li><li><a href="testimonials.html">Testimonials</a></li><li><a href="faqs.html">FAQs</a></li><li><a href="contact.html">Contact</a></li></ul></div>
    <div class="footer-col"><h3>Get in touch</h3><ul>
      <li><a href="tel:{C['phone_tel']}">{C['phone']}</a></li>
      <li><a href="{WA_HELLO}" target="_blank" rel="noopener">WhatsApp {C['wa_display']}</a></li>
      <li><a href="mailto:{C['email']}">{C['email']}</a></li>
      <li>{C['address']}</li>
      <li>{C['hours'][0][0]}: {C['hours'][0][1]}</li></ul></div>
  </div>
  <div class="footer-bottom"><span>&copy; <span data-year>2026</span> {esc(C['brand'])} All rights reserved.</span>
    <ul><li><a href="privacy-policy.html">Privacy Policy</a></li><li><a href="terms.html">Terms &amp; Conditions</a></li></ul></div>
</div></footer>
<a class="wa-float" href="{WA_HELLO}" target="_blank" rel="noopener" aria-label="Chat with us on WhatsApp">{wa_icon()}<span>WhatsApp</span></a>'''


def page(filename, title, desc, body, current=None, scripts=(), extra_head=""):
    current = current or filename
    scripts_html = "".join('<script src="assets/js/%s" defer></script>' % s for s in scripts)
    html = f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc, True)}">
<meta property="og:title" content="{esc(title, True)}">
<meta property="og:description" content="{esc(desc, True)}">
<meta property="og:type" content="website">
<meta name="theme-color" content="#0F1B3D">
<link rel="icon" href="assets/img/favicon.svg" type="image/svg+xml">
<link rel="preload" href="assets/fonts/fraunces-800.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="assets/css/fonts.css">
<link rel="stylesheet" href="assets/css/style.css">
<script>document.documentElement.classList.add('js');</script>
{extra_head}</head>
<body>
{header(current)}
<main id="main">
{body}
</main>
{footer()}
<script src="assets/js/site.js" defer></script>
{scripts_html}
</body>
</html>'''
    with open(os.path.join(ROOT, filename), "w", encoding="utf-8") as f:
        f.write(html)
    print("wrote", filename)


def page_hero(title, lead, crumbs, image=None, accent="#ffd84a"):
    bc = "".join('<li><a href="%s">%s</a></li>' % (h, l) for l, h in crumbs) + '<li aria-current="page">%s</li>' % esc(title)
    media = '<div class="page-hero-media">%s</div>' % image if image else ""
    return f'''<section class="page-hero" style="--accent:{accent}"><div class="container">
  <div class="page-hero-inner"><div class="page-hero-text">
    <ol class="breadcrumb" aria-label="Breadcrumb">{bc}</ol>
    <h1>{esc(title)}</h1><p class="lead">{lead}</p></div>{media}</div>
</div></section>'''


def section_head(eyebrow, title, lead="", center=False, light=False):
    cls = "section-head section-head--center" if center else "section-head"
    e = '<span class="eyebrow%s">%s</span>' % (" eyebrow--paper" if light else "", eyebrow) if eyebrow else ""
    return f'<div class="{cls} reveal">{e}<h2>{title}</h2>{"<p class=lead>%s</p>" % lead if lead else ""}</div>'


def testimonial_card(t):
    name, role = t[1], t[2]
    stars = "".join(icon("star") for _ in range(t[4]))
    return f'''<figure class="testimonial reveal" style="--tag:{t[3]}">
  <span class="stars" role="img" aria-label="{t[4]} out of 5 stars">{stars}</span>
  <blockquote class="testimonial-text" style="margin:0">{esc(t[0])}</blockquote>
  <figcaption class="testimonial-person"><span class="testimonial-avatar" aria-hidden="true">{esc(name[0])}</span><span><span class="testimonial-name">{esc(name)}</span><br><span class="testimonial-role">{esc(role)}</span></span></figcaption>
</figure>'''


def product_card(p):
    cat = CATS[p["cat"]]
    return f'''<article class="card reveal"><a class="card-media" href="{p['file']}" tabindex="-1" aria-hidden="true">{img(p['img'], p['name'])}</a>
  <div class="card-body"><span class="card-tag" style="--tag:{cat['tag']}">{esc(cat['name'])}</span><h3><a href="{p['file']}" style="text-decoration:none">{esc(p['short'])}</a></h3>
  <p>{esc(p['desc'].split('.')[0])}.</p>
  <a class="btn btn--small" href="{p['file']}">View details {icon('arrow')}</a></div></article>'''


def cta_strip(heading="Ready to order? Let&rsquo;s talk numbers."):
    return f'''<section class="section section--ink cta-strip" id="enquiry"><div class="container"><div class="row row--center">
  <div class="col reveal"><span class="eyebrow">Get a quote</span><h2>{heading}</h2>
    <p class="lead">Tell us what you need and we will come back with a written quote, usually within one working day.</p>
    <ul class="contact-line">
      <li>{icon('phone')}<span><strong>Call</strong><a href="tel:{C['phone_tel']}">{C['phone']}</a></span></li>
      <li>{wa_icon()}<span><strong>WhatsApp</strong><a href="{WA_HELLO}" target="_blank" rel="noopener">{C['wa_display']}</a></span></li>
      <li>{icon('mail')}<span><strong>Email</strong><a href="mailto:{C['email']}">{C['email']}</a></span></li></ul></div>
  <div class="col reveal"><div class="form-panel">
    <form class="form" data-mailto="{C['email']}" data-subject="Quote request from website">
      <div class="form-field"><label for="q-name">Name <span>*</span></label><input id="q-name" name="name" required autocomplete="name"></div>
      <div class="form-field"><label for="q-phone">Phone or email <span>*</span></label><input id="q-phone" name="contact" data-label="Phone / email" required></div>
      <div class="form-field form-field--full"><label for="q-need">What do you need?</label><textarea id="q-need" name="need" data-label="Requirement" placeholder="e.g. 200 ring binders A4, printed with our logo"></textarea></div>
      <button class="btn btn--primary" type="submit">Send quote request {icon('arrow')}</button>
      <p class="form-status" role="status" aria-live="polite"></p>
    </form></div></div>
</div></div></section>'''


def catalogue_banner():
    return f'''<section class="section"><div class="container"><div class="banner reveal">
  <div class="banner-text"><span class="eyebrow eyebrow--paper">Free download</span><h2>Take the whole range with you.</h2>
    <p>Our full product catalogue as a PDF: every category, sizes and pack quantities. Save it, share it with your buyers, or ask us for a printed copy.</p>
    <p></p><div class="btn-group"><a class="btn btn--primary" href="downloads/inkwell-catalogue.pdf" download>{icon('download')} Download catalogue (PDF)</a><a class="btn" style="background:transparent;color:var(--paper)" href="catalogue.html">See what&rsquo;s inside</a></div></div>
  <div class="banner-media"><div class="catalogue-cover" aria-hidden="true"><span>Catalogue {2026}</span><strong>{esc(C['brand'])}</strong><span>Office &amp; school stationery</span></div></div>
</div></div></section>'''


# ----------------------------------------------------------------- PAGES ---
def build_home():
    cats_marquee = ["Ring binders", "Ballpoint pens", "Whiteboards", "Laminators", "Sticky notes", "Box files", "Shredders", "Clipboards", "Lanyards", "Notice boards", "Labels", "Filing cabinets"]
    mq = "".join("<li>%s</li>" % m for m in cats_marquee)
    hero_cards = [("desk", "Office essentials", "Notebooks, pencils and glasses on a white desk"), ("binders", "Files &amp; folders", "Colourful ring binders on office shelves"), ("pencils-white", "School &amp; craft", "Colour pencils on a white surface")]
    hc = ""
    for n, (im, cap, alt) in enumerate(hero_cards, 1):
        hc += f'<figure class="hero-card hero-card--{n}">{img(im, alt, eager=True, sizes="(max-width:820px) 60vw, 26vw")}<figcaption>{cap}</figcaption></figure>'

    desk_pos = [("4%", "9%", "-5deg", "27%"), ("36%", "4%", "3deg", "27%"), ("67%", "12%", "-3deg", "27%"), ("14%", "52%", "4deg", "27%"), ("50%", "50%", "-4deg", "27%")]
    desk_items, desk_panels = "", ""
    for c, (x, y, r, w) in zip(CATS, desk_pos):
        desk_items += f'<a class="desk-item" href="{cat_page(c)}" data-category="{c["slug"]}" style="--x:{x};--y:{y};--r:{r};--w:{w};--tag:{c["tag"]}">{img(c["img"], c["alt"], sizes="20vw")}<span class="desk-item-label">{esc(c["name"])}</span></a>'
        chips = "".join('<li><a class="chip" href="%s#%s">%s</a></li>' % (cat_page(c), s["slug"], esc(s["name"])) for s in c["subs"][:6])
        if len(c["subs"]) > 6:
            chips += '<li><a class="chip" href="%s">+%d more</a></li>' % (cat_page(c), len(c["subs"]) - 6)
        desk_panels += f'''<article class="desk-panel" data-category-panel="{c["slug"]}" style="--tag:{c["tag"]}" hidden><h3>{esc(c["name"])}</h3><p>{esc(c["short"])}</p><ul>{chips}</ul><a class="btn btn--dark" href="{cat_page(c)}">Explore {esc(c["name"])} {icon("arrow")}</a></article>'''

    why = [("award", "Quality you can trust", "Every line is tested for durability so your team reorders with confidence.", "var(--c-office)"),
           ("tag", "Competitive bulk pricing", "Carton and pallet pricing that keeps your purchasing budget under control.", "var(--c-files)"),
           ("truck", "Fast delivery", "In-stock items dispatched in one to two working days across the UAE.", "var(--c-equip)"),
           ("palette", "Custom branding", "Your logo on files, binders, folders, lanyards and more.", "var(--c-boards)"),
           ("layers", "One wide range", "From pens to shredders, one supplier replaces five.", "var(--c-school)")]
    why_html = "".join(f'<div class="icon-box reveal" style="--tag:{t}"><span class="icon-box-icon">{icon(i)}</span><h3>{h}</h3><p>{p}</p></div>' for i, h, p, t in why)

    inds = [("briefcase", "Corporate", "Offices, agencies and head offices that reorder every month."),
            ("book", "Schools", "Nurseries to universities, with back-to-school bulk packs."),
            ("landmark", "Government", "Departments and authorities with tender-ready paperwork."),
            ("coffee", "Hospitality", "Hotels and restaurants: printed folders, pads and lanyards."),
            ("store", "Retail &amp; resale", "Bookshops and resellers who need dependable wholesale stock.")]
    inds_html = "".join(f'<div class="industry reveal">{icon(i)}<h3>{h}</h3><p>{p}</p></div>' for i, h, p in inds)

    steps = [("Start with a blank", "A plain binder straight from stock, ready to become yours.", "#8a93a6", "off", "none"),
             ("Choose your colour", "Pick from our standard range or match a brand colour on larger runs.", "#2453d6", "off", "none"),
             ("Add your logo", "Send your artwork. We proof it, you approve it, we print it.", "#2453d6", "on", "none"),
             ("Finish with foil", "Foil stamping or embossing gives an executive, premium finish.", "#2453d6", "on", "foil")]
    steps_html = "".join(f'<li class="brand-step" data-binder-color="{c}" data-logo="{l}" data-finish="{f}"><span class="brand-step-number">{n}</span><div><h3 class="brand-step-title">{h}</h3><p class="brand-step-text">{p}</p></div></li>' for n, (h, p, c, l, f) in enumerate(steps, 1))
    swatches = "".join(f'<span class="brand-swatch" style="--sw:{c}" data-color="{c}"></span>' for c in ["#8a93a6", "#2453d6", "#e5484d", "#1f9d74"])

    body = f'''<section class="hero"><div class="container"><div class="hero-inner">
  <div class="hero-copy">
    <span class="eyebrow hero-fade">Office &amp; school stationery &middot; {C['city']}</span>
    <div class="hero-headline-wrap">
      <h1 class="hero-headline">Equipping offices and schools with stationery that <span class="hl-mark">means business.</span></h1>
      <svg class="hero-pen" viewBox="0 0 46 46" aria-hidden="true"><path d="M6 40 8.500 31.500 37 3l6 6-28.500 28.500z" fill="#FFD84A" stroke="#FBF7EF" stroke-width="2.500" stroke-linejoin="round"/><path d="M6 40 8.500 31.500l6 6z" fill="#0F1B3D"/></svg>
    </div>
    <p class="hero-lead hero-fade">Quality files, pens, boards and equipment for teams that order in bulk, with sharp pricing, fast delivery and your logo on request.</p>
    <div class="btn-group hero-actions hero-fade"><a class="btn btn--primary" href="products.html">Explore Products {icon('arrow')}</a><a class="btn" href="{quote_link()}">Request a Quote</a></div>
    <ul class="hero-proof hero-fade"><li>{icon('check')} Bulk &amp; carton pricing</li><li>{icon('check')} Custom logo printing</li><li>{icon('check')} Delivery across {C['country']}</li></ul>
  </div>
  <div class="hero-stack">{hc}<div class="hero-sticker hero-fade" aria-hidden="true">Bulk pricing on request</div></div>
</div></div></section>

<section class="trust" aria-label="Key figures"><div class="container"><div class="row row--tight">
  <div class="stat"><span class="stat-number">{C['years']}</span><span class="stat-label">Years in business</span></div>
  <div class="stat"><span class="stat-number">{C['products']}</span><span class="stat-label">Products in stock</span></div>
  <div class="stat"><span class="stat-number">{C['clients']}</span><span class="stat-label">Clients served</span></div>
  <div class="stat"><span class="stat-number">{C['coverage']}</span><span class="stat-label">Delivery coverage</span></div>
</div></div></section>

<div class="marquee" aria-hidden="true"><div class="marquee-track"><ul class="marquee-group">{mq}</ul><ul class="marquee-group">{mq}</ul></div></div>

<section class="section" id="categories"><div class="container">
  {section_head("Shop by category", "Five departments. One desk to explore.", "Hover or tap an item on the desk to preview the category. Click to see everything inside.")}
  <div class="desk">
    <div class="desk-scene">{desk_items}<p class="desk-hint">Hover or tap a category</p></div>
    <div class="desk-panels">{desk_panels}</div>
  </div>
</div></section>

<section class="section section--paper2" id="featured"><div class="container">
  {section_head("Featured &amp; new", "Best-sellers our clients reorder.", "A taste of the range. Every product page has options, specs and a one-click quote request.")}
  <div class="card-row card-row--4">
    {"".join(product_card(p) for p in PRODUCTS)}
    <article class="card reveal"><a class="card-media" href="customisation.html" tabindex="-1" aria-hidden="true">{img("binders", "Custom-printed ring binders", pos="90% 50%")}</a>
      <div class="card-body"><span class="card-tag" style="--tag:var(--c-files)">Custom</span><h3><a href="customisation.html" style="text-decoration:none">Logo-printed files &amp; binders</a></h3><p>Your brand on every file, from 100 pieces.</p><a class="btn btn--small" href="customisation.html">How it works {icon('arrow')}</a></div></article>
  </div>
</div></section>

<section class="section" id="why"><div class="container">
  {section_head("Why choose us", "Stationery is simple. Reliable suppliers aren&rsquo;t.", "Here is what buyers tell us they value most.")}
  <div class="row row--tight" style="gap:22px">{why_html}</div>
</div></section>

<section class="section section--ink brand" id="customisation" aria-labelledby="brand-title">
  <div class="brand-scroll"><div class="brand-sticky"><div class="container brand-inner">
    <div class="brand-copy">
      <span class="eyebrow">Corporate branding</span>
      <h2 id="brand-title">Plain binder in. Your brand out.</h2>
      <p class="lead">Scroll to watch a stock binder become yours. Custom-printed files, binders and folders from 100 pieces.</p>
      <ol class="brand-steps">{steps_html}</ol>
      <div class="btn-group"><a class="btn btn--primary" href="customisation.html">See the branding process {icon('arrow')}</a><a class="btn" style="background:transparent;color:var(--paper)" href="{quote_link('Custom branded files')}">Get a custom quote</a></div>
    </div>
    <div class="brand-stage">
      <div class="brand-binder" data-logo="on" data-finish="foil" style="--binder-color:#2453d6" role="img" aria-label="Illustration of a ring binder being customised with a logo">
        <div class="binder-cover">
          <div class="binder-spine"></div>
          <div class="binder-rings"><span class="binder-ring"></span><span class="binder-ring"></span><span class="binder-ring"></span></div>
          <div class="binder-logo"><svg viewBox="0 0 40 40" aria-hidden="true"><path d="M20 4 32 20 20 36 8 20z" fill="currentColor"/><circle cx="20" cy="17" r="3.5" fill="var(--binder-color)"/><path d="M20 20v10" stroke="var(--binder-color)" stroke-width="3"/></svg><span class="binder-logo-name">{esc(C['brand'])}</span><span class="binder-logo-tag">Your logo here</span></div>
          <div class="binder-label">Your company name</div>
          <div class="binder-shine"></div>
        </div>
      </div>
      <div class="brand-swatches" aria-hidden="true">{swatches}</div>
    </div>
  </div></div></div>
</section>

<section class="section" id="industries"><div class="container">
  {section_head("Industries we serve", "Supplying the people who keep things running.")}
  <div class="row" style="gap:28px">{inds_html}</div>
</div></section>

<section class="section section--paper2" id="testimonials"><div class="container">
  {section_head("Testimonials", "Trusted by buyers who reorder.", "", center=True)}
  <div class="row">{"".join(testimonial_card(t) for t in TESTIMONIALS[:3])}</div>
  <p style="text-align:center;margin:36px 0 0"><a class="btn btn--dark" href="testimonials.html">Read more reviews {icon('arrow')}</a></p>
</div></section>

{catalogue_banner()}
{cta_strip()}'''
    org = json.dumps({"@context": "https://schema.org", "@type": "Organization", "name": C["brand"], "email": C["email"], "telephone": C["phone"],
                      "address": {"@type": "PostalAddress", "streetAddress": C["address"], "addressCountry": C["country"]},
                      "description": "Office and school stationery supplier: files, binders, boards and equipment in bulk."}, indent=0)
    page("index.html", "Office & School Stationery Supplier in %s | Wholesale | %s" % (C["city"], C["brand"]),
         "%s supplies office and school stationery in bulk across %s: files, binders, boards, equipment and custom-printed folders. Request a quote today." % (C["brand"], C["country"]),
         body, "index.html", ("hero-writer.js", "desk-explorer.js", "brand-binder.js"),
         '<script type="application/ld+json">%s</script>\n' % org)


def build_products():
    cards = ""
    for c in CATS:
        chips = "".join('<li><a class="chip" href="%s#%s">%s</a></li>' % (cat_page(c), s["slug"], esc(s["name"])) for s in c["subs"])
        cards += f'''<article class="card reveal"><a class="card-media" href="{cat_page(c)}" tabindex="-1" aria-hidden="true">{img(c['img'], c['alt'])}</a>
  <div class="card-body" style="--tag:{c['tag']}"><span class="card-tag" style="--tag:{c['tag']}">{len(c['subs'])} sub-categories</span><h2 style="font-size:1.8rem"><a href="{cat_page(c)}" style="text-decoration:none">{esc(c['name'])}</a></h2><p>{esc(c['short'])}</p>
  <ul style="list-style:none;display:flex;flex-wrap:wrap;gap:8px;margin:6px 0 10px">{chips}</ul>
  <a class="btn btn--dark btn--small" href="{cat_page(c)}">Browse {esc(c['name'])} {icon('arrow')}</a></div></article>'''
    feat = "".join(product_card(p) for p in PRODUCTS)
    body = page_hero("Our products", "Five departments covering everything an office or school needs. Browse a category, open a product, then request a quote in a click.", [("Home", "index.html")]) + f'''
<section class="section"><div class="container">{section_head("Categories", "Find what you need.")}<div class="card-row card-row--2">{cards}</div></div></section>
<section class="section section--paper2"><div class="container">{section_head("Featured", "Popular right now.")}<div class="card-row card-row--3">{feat}</div></div></section>
{catalogue_banner()}'''
    page("products.html", "Office & School Stationery Products | %s" % C["brand"], "Browse office products, files and folders, office equipment, boards and display, and school, art and craft supplies. Bulk pricing and custom branding available.", body)


def build_category(c):
    cards = ""
    for s in c["subs"]:
        cards += f'''<article class="card reveal" id="{s['slug']}"><div class="card-media">{img(s['img'], s['name'] + ' stationery', pos=s['pos'])}</div>
  <div class="card-body"><h3>{esc(s['name'])}</h3><p>{esc(s['desc'])}</p>
  <a class="btn btn--small" href="{quote_link(s['name'])}">Enquire {icon('arrow')}</a></div></article>'''
    others = "".join('<li><a class="chip" href="%s">%s</a></li>' % (cat_page(o), esc(o["name"])) for o in CATS if o is not c)
    body = page_hero(c["name"], esc(c["intro"]), [("Home", "index.html"), ("Products", "products.html")], img(c["img"], c["alt"], eager=True), c["accent"]) + f'''
<section class="section"><div class="container">{section_head("Sub-categories", "What&rsquo;s in %s" % esc(c["name"]), esc(c["tagline"]))}
  <div class="card-row">{cards}</div></div></section>
<section class="section section--paper2"><div class="container"><div class="row row--center">
  <div class="col reveal"><h2 style="font-size:clamp(1.6rem,3vw,2.4rem)">Can&rsquo;t see the exact item?</h2><p class="lead">Our full range is much bigger than this page. Tell us what you need and we will source it.</p>
  <div class="btn-group"><a class="btn btn--primary" href="{quote_link()}">Request a Quote</a><a class="btn btn--wa" href="{wa_link('Hi, I am looking for ' + c['name'] + ' products.')}" target="_blank" rel="noopener">{wa_icon()} WhatsApp us</a></div></div>
  <div class="col reveal"><h3>Other categories</h3><ul style="list-style:none;display:flex;flex-wrap:wrap;gap:10px">{others}</ul></div>
</div></div></section>'''
    page(cat_page(c), "%s: Wholesale Supplier in %s | %s" % (c["name"], C["city"], C["brand"]),
         "%s from %s: %s Bulk pricing, fast delivery and custom branding. Request a quote." % (c["name"], C["brand"], c["short"]), body)


def build_product(p):
    cat = CATS[p["cat"]]
    thumbs = "".join(f'<button class="gallery-thumb{" is-active" if i == 0 else ""}" type="button" data-gallery-thumb="assets/img/{g}.jpg" data-alt="{esc(a, True)}" aria-label="Show photo {i+1}">{img(g, a)}</button>' for i, (g, a) in enumerate(p["gallery"]))
    opts = ""
    for key, label, values in p["options"]:
        btns = ""
        for i, v in enumerate(values):
            pressed = "true" if i == 0 else "false"
            if isinstance(v, tuple):
                btns += f'<button type="button" class="option" data-value="{esc(v[0], True)}" aria-pressed="{pressed}"><span class="option-swatch" style="--sw:{v[1]}"></span>{esc(v[0])}</button>'
            else:
                btns += f'<button type="button" class="option" data-value="{esc(v, True)}" aria-pressed="{pressed}">{esc(v)}</button>'
        opts += f'<div class="option-group" data-option="{label}" role="group" aria-label="{label}"><div class="option-label">{label}: <span></span></div><div class="option-list">{btns}</div></div>'
    specs = "".join("<tr><th scope=\"row\">%s</th><td>%s</td></tr>" % (esc(a), esc(b)) for a, b in p["specs"])
    feats = "".join("<li>%s%s</li>" % (icon("check"), esc(f)) for f in p["features"])
    rel = "".join(product_card(q) for q in PRODUCTS if q["slug"] in p["related"])
    rel += f'''<article class="card reveal"><a class="card-media" href="customisation.html" tabindex="-1" aria-hidden="true">{img("binders", "Custom-printed binders", pos="90% 50%")}</a><div class="card-body"><span class="card-tag" style="--tag:var(--c-files)">Custom</span><h3><a href="customisation.html" style="text-decoration:none">Add your logo</a></h3><p>Print your brand on files, binders and folders.</p><a class="btn btn--small" href="customisation.html">How it works {icon('arrow')}</a></div></article>'''
    body = f'''<div class="container" style="padding-top:26px"><ol class="breadcrumb breadcrumb--dark" aria-label="Breadcrumb"><li><a href="index.html">Home</a></li><li><a href="products.html">Products</a></li><li><a href="{cat_page(cat)}">{esc(cat['name'])}</a></li><li aria-current="page">{esc(p['short'])}</li></ol></div>
<section class="section" style="padding-top:20px"><div class="container"><div class="product" data-product="{esc(p['name'], True)}">
  <div class="gallery"><div class="gallery-main">{img(p['gallery'][0][0], p['gallery'][0][1], eager=True)}</div><div class="gallery-thumbs">{thumbs}</div></div>
  <div class="product-info">
    <div><span class="badge">{esc(p['badge'])}</span></div>
    <h1>{esc(p['name'])}</h1>
    <span class="product-sku">SKU {p['sku']} &middot; <a href="{cat_page(cat)}">{esc(cat['name'])}</a></span>
    <p class="lead" style="margin:0">{esc(p['desc'])}</p>
    {opts}
    <div class="product-actions"><a class="btn btn--primary" href="{quote_link(p['name'])}" data-quote-link="contact.html">Request a Quote {icon('arrow')}</a>
      <a class="btn btn--wa" href="{wa_link('Hi, I would like a quote for: ' + p['name'])}" data-wa-link="{WA_BASE}" target="_blank" rel="noopener">{wa_icon()} WhatsApp</a></div>
    <p class="product-note">{icon('truck')} Bulk pricing and fast UAE delivery. Custom branding available.</p>
  </div>
</div></div></section>
<section class="section section--paper2"><div class="container"><div class="row">
  <div class="col--wide col reveal"><h2 style="font-size:2rem">Specifications</h2><div class="table-wrap"><table class="table-specs"><tbody>{specs}</tbody></table></div></div>
  <div class="col reveal"><h2 style="font-size:2rem">Why buyers pick it</h2><ul class="check-list">{feats}</ul></div>
</div></div></section>
<section class="section"><div class="container">{section_head("You may also need", "Related products")}<div class="card-row card-row--3">{rel}</div></div></section>
{cta_strip("Want this in bulk? Get your quote.")}'''
    page(p["file"], p["title"], p["meta"], body, p["file"], ("site.js",) if False else ())


def build_about():
    body = page_hero("About us", "A family of stationery people supplying the offices and schools of %s since day one." % C["country"], [("Home", "index.html")], img("warehouse", "Warehouse shelves stacked with boxes", eager=True)) + f'''
<section class="section"><div class="container"><div class="row row--center">
  <div class="col reveal"><span class="eyebrow">Our story</span><h2>From one shelf to a full-range supplier.</h2>
    <p class="lead">Placeholder story: {esc(C['brand'])} began as a small stationery counter serving nearby offices. Today we supply corporates, schools, government departments and retailers across {C['country']}.</p>
    <p>Replace this text with your real history: who founded the company, why, and what you stand for. Buyers trust suppliers who show the people behind the products.</p>
    <p>We stock thousands of lines, pack every order carefully and treat every quote as a promise.</p></div>
  <div class="col reveal">{img("team", "Team gathered around a table with pens", cls="photo photo--tilt", sizes="(max-width:800px) 100vw, 40vw")}</div>
</div></div></section>
<section class="trust"><div class="container"><div class="row row--tight">
  <div class="stat"><span class="stat-number">{C['years']}</span><span class="stat-label">Years in business</span></div>
  <div class="stat"><span class="stat-number">{C['products']}</span><span class="stat-label">Products in stock</span></div>
  <div class="stat"><span class="stat-number">{C['clients']}</span><span class="stat-label">Clients served</span></div>
  <div class="stat"><span class="stat-number">{C['coverage']}</span><span class="stat-label">Delivery coverage</span></div>
</div></div></section>
<section class="section section--paper2"><div class="container"><div class="row row--center">
  <div class="col reveal">{img("warehouse", "Large warehouse with racks of stock", cls="photo", sizes="(max-width:800px) 100vw, 45vw")}</div>
  <div class="col reveal"><span class="eyebrow">Our facility</span><h2>Stock on the shelf, ready to ship.</h2>
    <p class="lead">Placeholder facility text: our warehouse holds deep stock of the fastest-moving lines, so most orders leave within one to two working days.</p>
    <ul class="check-list"><li>{icon('check')}Warehouse of X sq ft (add your real size)</li><li>{icon('check')}Dedicated packing and dispatch team</li><li>{icon('check')}Own delivery fleet across {C['country']}</li></ul></div>
</div></div></section>
<section class="section"><div class="container">{section_head("Milestones", "How we got here.")}
  <ol class="timeline reveal"><li><strong>Year one</strong>Placeholder: opened our first stationery counter.</li><li><strong>Year five</strong>Placeholder: first school and government contracts.</li><li><strong>Year eight</strong>Placeholder: moved into a larger warehouse and launched custom branding.</li><li><strong>Today</strong>Placeholder: serving {C['clients']} clients with {C['products']} products.</li></ol></div></section>
<section class="section section--ink"><div class="container">{section_head("Why choose us", "Five reasons buyers stay.", light=True)}
  <div class="row row--tight" style="gap:22px">
  {"".join(f'<div class="icon-box reveal" style="--tag:{t}"><span class="icon-box-icon" style="color:var(--ink)">{icon(i)}</span><h3>{h}</h3><p>{p}</p></div>' for i, h, p, t in [("award", "Quality", "Consistent, tested products.", "var(--c-office)"), ("tag", "Bulk pricing", "Carton and pallet rates.", "var(--c-files)"), ("truck", "Fast delivery", "In-stock items in 1 to 2 days.", "var(--c-equip)"), ("palette", "Customisation", "Your logo on files and more.", "var(--c-boards)"), ("layers", "Wide range", "One supplier, every category.", "var(--c-school)")])}
  </div></div></section>
{cta_strip("Let&rsquo;s work together.")}'''
    page("about.html", "About %s | Office & School Stationery Supplier" % C["brand"], "Learn about %s: our story, our warehouse and why offices, schools and retailers across %s trust us for bulk stationery supply." % (C["brand"], C["country"]), body)


def build_customisation():
    steps = [("upload", "Send your artwork", "Share your logo as a vector file (AI, EPS, PDF) or a high-resolution PNG."),
             ("palette", "Choose product &amp; finish", "Pick the file, binder or folder, its colour, and a print method."),
             ("eye", "Approve the proof", "We send a digital proof within one working day. Nothing prints until you approve."),
             ("pen", "We produce", "Printing, foil or embossing in our production partners&rsquo; workshop. Typically 10 to 15 working days."),
             ("package", "Delivered to you", "Packed in cartons, labelled and delivered to your door.")]
    steps_html = "".join(f'<div class="step reveal"><span class="step-number">{n}</span><h3>{h}</h3><p>{p}</p></div>' for n, (i, h, p) in enumerate(steps, 1))
    ex = [("binders", "Executive binders", "Navy PVC with silver foil logo on the spine and cover.", "80% 50%"),
          ("folders", "Presentation folders", "Full-colour printed cover with a matching business card slot.", "50% 50%"),
          ("clipboard", "Branded clipboards", "Colour-matched boards for site teams and events.", "50% 40%")]
    ex_html = "".join(f'<div class="example-swatch reveal">{img(i, t, pos=pos)}<h3>{t}</h3><p>{d}</p></div>' for i, t, d, pos in ex)
    body = page_hero("Customisation & corporate branding", "Files, binders and folders that carry your logo. Ideal for corporate gifting, client packs, school branding and event kits.", [("Home", "index.html")], img("binders", "Ring binders in a row on an office shelf", eager=True), "#ff7a66") + f'''
<section class="section"><div class="container">{section_head("The process", "From logo to delivered, in five steps.")}<div class="row" style="gap:32px">{steps_html}</div></div></section>
<section class="section section--paper2"><div class="container"><div class="row">
  <div class="col reveal"><div class="form-panel" style="height:100%"><span class="eyebrow">Minimum order</span><h2 style="font-size:2rem">What you need to know</h2>
    <div class="table-wrap" style="box-shadow:none"><table class="table-specs"><tbody>
      <tr><th scope="row">Minimum order</th><td>100 pieces (placeholder: confirm)</td></tr>
      <tr><th scope="row">Print methods</th><td>Screen print, foil stamp, emboss, digital</td></tr>
      <tr><th scope="row">Artwork</th><td>AI, EPS, vector PDF or 300 dpi PNG</td></tr>
      <tr><th scope="row">Proof</th><td>Digital proof within 1 working day</td></tr>
      <tr><th scope="row">Lead time</th><td>10 to 15 working days after approval</td></tr></tbody></table></div></div></div>
  <div class="col reveal"><span class="eyebrow">Good to know</span><h2 style="font-size:2rem">Made for repeat buyers.</h2>
    <ul class="check-list"><li>{icon('check')}We store your approved artwork for easy reorders</li><li>{icon('check')}Colour matching for larger runs</li><li>{icon('check')}Mixed-size runs on request</li><li>{icon('check')}Ideal for corporate gifts, client packs and schools</li></ul>
    <div class="btn-group" style="margin-top:24px"><a class="btn btn--primary" href="{quote_link('Custom branded files')}">Start a custom quote {icon('arrow')}</a><a class="btn btn--wa" href="{wa_link('Hi, I would like to customise files with our logo.')}" target="_blank" rel="noopener">{wa_icon()} WhatsApp</a></div></div>
</div></div></section>
<section class="section"><div class="container">{section_head("Examples", "What custom looks like.")}<div class="row" style="gap:32px">{ex_html}</div></div></section>
{cta_strip("Tell us about your branding project.")}'''
    page("customisation.html", "Custom Printed Files, Binders & Folders with Your Logo | %s" % C["brand"], "Custom-printed files, binders and folders with your company logo. Screen print, foil and emboss options, low minimums and a simple proof process. Request a quote.", body)


def build_catalogue():
    body = page_hero("Product catalogue", "Download the full range as a PDF. Every category, size and pack quantity in one place.", [("Home", "index.html")]) + f'''
<section class="section"><div class="container"><div class="row row--center">
  <div class="col reveal" style="display:flex;justify-content:center"><div class="catalogue-cover" style="width:260px" aria-hidden="true"><span>Catalogue 2026</span><strong style="font-size:2rem">{esc(C['brand'])}</strong><span>Office &amp; school stationery</span></div></div>
  <div class="col reveal"><span class="eyebrow">Free PDF</span><h2>Everything we stock, in your pocket.</h2>
    <p class="lead">Save it to your phone, forward it to your buyers or print the pages you need.</p>
    <ul class="check-list"><li>{icon('check')}Five categories with sub-categories</li><li>{icon('check')}Sizes, colours and pack quantities</li><li>{icon('check')}Customisation options and minimum orders</li></ul>
    <div class="btn-group" style="margin-top:28px"><a class="btn btn--primary" href="downloads/inkwell-catalogue.pdf" download>{icon('download')} Download catalogue (PDF)</a><a class="btn" href="{quote_link('Printed catalogue')}">Request a printed copy</a></div>
    <p style="font-size:0.9rem;color:var(--ink-soft);margin-top:16px">Placeholder catalogue: replace <strong>downloads/inkwell-catalogue.pdf</strong> with your real PDF.</p></div>
</div></div></section>
{cta_strip()}'''
    page("catalogue.html", "Download Our Stationery Catalogue (PDF) | %s" % C["brand"], "Download the %s stationery catalogue as a PDF: office products, files and folders, equipment, boards and school supplies." % C["brand"], body)


def build_faqs():
    items = "".join(f'<details class="accordion-item reveal"><summary>{esc(q)}</summary><div class="accordion-body"><p>{esc(a)}</p></div></details>' for q, a in FAQS)
    ld = json.dumps({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FAQS]})
    body = page_hero("Frequently asked questions", "Quick answers about ordering, delivery, customisation and payment.", [("Home", "index.html")]) + f'''
<section class="section"><div class="container"><div class="accordion">{items}</div>
  <div style="text-align:center;margin-top:48px" class="reveal"><h2 style="font-size:1.8rem">Still have a question?</h2><div class="btn-group" style="justify-content:center"><a class="btn btn--primary" href="contact.html">Contact us</a><a class="btn btn--wa" href="{WA_HELLO}" target="_blank" rel="noopener">{wa_icon()} WhatsApp</a></div></div></div></section>'''
    page("faqs.html", "Stationery Ordering FAQs | %s" % C["brand"], "Answers to common questions about bulk stationery orders, custom printing, delivery times and payment terms at %s." % C["brand"], body, extra_head='<script type="application/ld+json">%s</script>\n' % ld)


def build_testimonials():
    body = page_hero("Testimonials", "What corporate buyers, schools, retailers and government teams say about working with us.", [("Home", "index.html")]) + f'''
<section class="section"><div class="container">
  <div class="row row--center reveal" style="margin-bottom:44px"><div class="stat" style="flex:0 0 auto"><span class="stat-number">4.9</span><span class="stat-label">Average rating (placeholder)</span></div><span class="stars" role="img" aria-label="5 stars" style="font-size:1.6rem">{"".join(icon('star') for _ in range(5))}</span></div>
  <div class="row">{"".join(testimonial_card(t) for t in TESTIMONIALS)}</div>
  <p style="font-size:0.9rem;color:var(--ink-soft);margin-top:24px">These are placeholder reviews. Replace them with real client feedback (with permission).</p></div></section>
{cta_strip("Join our happy clients.")}'''
    page("testimonials.html", "Client Testimonials | %s" % C["brand"], "Read what businesses, schools, retailers and government teams say about ordering bulk stationery from %s." % C["brand"], body)


def build_contact():
    hours = "".join("<li><span>%s</span><strong>%s</strong></li>" % (d, t) for d, t in C["hours"])
    body = page_hero("Contact us", "Request a quote, ask a question or place an order. We reply within one working day.", [("Home", "index.html")]) + f'''
<section class="section" id="quote"><div class="container"><div class="row">
  <div class="col col--wide reveal"><div class="form-panel"><h2 style="font-size:2rem">Request a quote</h2>
    <form class="form" data-mailto="{C['email']}" data-subject="Quote request from website" id="quote-form">
      <div class="form-field"><label for="f-name">Full name <span>*</span></label><input id="f-name" name="name" required autocomplete="name"></div>
      <div class="form-field"><label for="f-company">Company / school</label><input id="f-company" name="company" autocomplete="organization"></div>
      <div class="form-field"><label for="f-email">Email <span>*</span></label><input id="f-email" name="email" type="email" required autocomplete="email"></div>
      <div class="form-field"><label for="f-phone">Phone / WhatsApp</label><input id="f-phone" name="phone" type="tel" autocomplete="tel"></div>
      <div class="form-field"><label for="f-type">I am a</label><select id="f-type" name="type"><option>Corporate buyer</option><option>School</option><option>Government office</option><option>Retailer / reseller</option><option>Other</option></select></div>
      <div class="form-field"><label for="f-product">Product or category</label><input id="f-product" name="product" data-prefill="product" placeholder="e.g. A4 ring binders"></div>
      <div class="form-field"><label for="f-qty">Approx. quantity</label><input id="f-qty" name="quantity" data-prefill="qty" placeholder="e.g. 200 pieces"></div>
      <div class="form-field form-field--full"><label for="f-msg">Details</label><textarea id="f-msg" name="message" data-prefill="details" placeholder="Sizes, colours, delivery location, deadline&hellip;"></textarea></div>
      <label class="form-check"><input type="checkbox" name="customisation" data-label="Needs customisation / logo printing"> I need custom logo printing</label>
      <button class="btn btn--primary" type="submit">Send request {icon('arrow')}</button>
      <p class="form-note">Submitting opens your email app with everything filled in. Just press send.</p>
      <p class="form-status" role="status" aria-live="polite"></p>
    </form></div></div>
  <div class="col reveal"><h2 style="font-size:2rem">Talk to us</h2>
    <ul class="contact-line" style="margin-bottom:28px">
      <li>{icon('phone')}<span><strong>Phone</strong><a href="tel:{C['phone_tel']}">{C['phone']}</a></span></li>
      <li>{wa_icon()}<span><strong>WhatsApp</strong><a href="{WA_HELLO}" target="_blank" rel="noopener">{C['wa_display']}</a></span></li>
      <li>{icon('mail')}<span><strong>Email</strong><a href="mailto:{C['email']}">{C['email']}</a></span></li>
      <li>{icon('pin')}<span><strong>Address</strong>{C['address']}</span></li></ul>
    <h3>{icon('clock')} Working hours</h3><ul class="hours">{hours}</ul>
    <div class="btn-group" style="margin-top:28px"><a class="btn btn--wa" href="{WA_HELLO}" target="_blank" rel="noopener">{wa_icon()} Chat on WhatsApp</a></div></div>
</div></div></section>
<section class="section section--paper2"><div class="container"><div class="row"><div class="col reveal" style="min-height:380px">
  <iframe class="map-frame" title="Map showing our location in {C['city']}" src="https://maps.google.com/maps?q={urllib.parse.quote(C['address'])}&amp;output=embed" loading="lazy" referrerpolicy="no-referrer-when-downgrade" allowfullscreen></iframe></div></div></div></section>'''
    page("contact.html", "Contact %s | Request a Stationery Quote in %s" % (C["brand"], C["city"]), "Contact %s to request a quote, call, email or WhatsApp. Find our address, working hours and map." % C["brand"], body)


def legal(filename, title, sections, desc):
    inner = "".join("<h2>%s</h2>%s" % (h, t) for h, t in sections)
    body = page_hero(title, "Last updated: %s. Placeholder text: have this reviewed by a legal professional before publishing." % "26 September 2026", [("Home", "index.html")]) + f'<section class="section"><div class="container"><div class="prose reveal">{inner}</div></div></section>'
    page(filename, "%s | %s" % (title, C["brand"]), desc, body)


def build_legal():
    b = C["brand"]
    legal("privacy-policy.html", "Privacy Policy", [
        ("Who we are", "<p>%s (&ldquo;we&rdquo;) supplies office and school stationery. This policy explains what personal information we collect through this website and how we use it.</p>" % esc(b)),
        ("Information we collect", "<p>We collect only what you send us: your name, company, email, phone number and the details of your enquiry when you use our forms, email, phone or WhatsApp.</p>"),
        ("How we use it", "<ul><li>To reply to enquiries and prepare quotations</li><li>To process and deliver orders</li><li>To send you the catalogue or updates you have asked for</li></ul>"),
        ("Forms and email", "<p>Our website forms open your own email application with the details pre-filled. Nothing is stored on this website itself. Your message is sent from your email account to ours.</p>"),
        ("Sharing", "<p>We do not sell your data. We share it only with delivery partners and service providers who need it to fulfil your order.</p>"),
        ("Cookies", "<p>This website does not use tracking cookies. Placeholder: update this section if you add analytics.</p>"),
        ("Your rights", "<p>You can ask us to access, correct or delete the information we hold about you by emailing %s.</p>" % C["email"]),
        ("Contact", "<p>Questions about this policy? Email <a href=\"mailto:%s\">%s</a>.</p>" % (C["email"], C["email"]))],
        "How %s collects, uses and protects your personal information when you contact us or request a quote." % b)
    legal("terms.html", "Terms & Conditions", [
        ("About these terms", "<p>By using this website and ordering from %s you agree to these terms. Placeholder text: replace with terms approved by your legal advisor.</p>" % esc(b)),
        ("Quotations and prices", "<p>Quotations are valid for the period stated on the quote. Prices exclude VAT unless stated and may change with supplier costs.</p>"),
        ("Orders", "<p>An order is accepted when we confirm it in writing. Customised orders require approval of artwork and proof before production begins and cannot be cancelled once production has started.</p>"),
        ("Payment", "<p>Payment terms are stated on your quotation or invoice. Goods remain our property until paid in full.</p>"),
        ("Delivery", "<p>Delivery dates are estimates. We are not liable for delays outside our control. Please inspect goods on delivery and report damage within 48 hours.</p>"),
        ("Returns", "<p>Standard stock items may be returned within 7 days if unused and in original packaging. Customised items are non-returnable unless faulty.</p>"),
        ("Liability", "<p>Our liability is limited to the value of the goods supplied, to the extent permitted by law.</p>"),
        ("Governing law", "<p>These terms are governed by the laws of %s.</p>" % C["country"])],
        "Terms and conditions for quotations, orders, customisation, delivery and returns with %s." % b)


def build_extras():
    with open(os.path.join(ROOT, "assets", "img", "favicon.svg"), "w", encoding="utf-8") as f:
        f.write('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 40 40"><rect x="2" y="2" width="36" height="36" rx="10" fill="#0F1B3D"/><path d="M20 7.5 28 20l-8 12.5L12 20z" fill="#FFD84A"/><circle cx="20" cy="18.5" r="2.6" fill="#0F1B3D"/></svg>')
    with open(os.path.join(ROOT, "robots.txt"), "w") as f:
        f.write("User-agent: *\nAllow: /\n# Add: Sitemap: https://YOUR-DOMAIN/sitemap.xml\n")


if __name__ == "__main__":
    build_extras()
    build_home()
    build_products()
    for c in CATS:
        build_category(c)
    for p in PRODUCTS:
        build_product(p)
    build_about()
    build_customisation()
    build_catalogue()
    build_faqs()
    build_testimonials()
    build_contact()
    build_legal()
