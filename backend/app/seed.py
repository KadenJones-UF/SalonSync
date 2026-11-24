"""Database seeding CLI command and authentic salon formulation fixtures.

Provides reproducible, realistic salon demo data for stylists, formulas, and moderators.
Supports the CEN 3031 Sprint 2 presentation walkthrough.
"""
from datetime import datetime, timedelta, timezone
import click
from flask.cli import with_appcontext

from .extensions import db
from .models.note import Note
from .models.user import User

# Authentic Cosmetology Formulations Dataset
# Real formulations using standard brands, true shade nomenclature, realistic developers and timing.
SEED_FORMULAS = [
    # ---- REDKEN SHADES EQ & COLOR GELS OILS ----
    {
        "title": "Sarah M. - Root Melt & Bronde Gloss",
        "brand": "Redken",
        "shades": "06N + 06T (Roots) / 09NB + 09GI (Zone 2/3)",
        "developer": "10 vol",
        "processing_time": 20,
        "notes": "Apply zone 1 formula with processing solution first. Melt zone 2/3 down for seamless blonde transition. Process 20 min on damp hair.",
        "is_public": True,
        "user_index": 0
    },
    {
        "title": "Emily K. - Icy Platinum Toner",
        "brand": "Redken",
        "shades": "010VV + 010P Lavender Ice",
        "developer": "5 vol",
        "processing_time": 15,
        "notes": "Pre-lightened to level 10 raw yellow. Apply toner at shampoo bowl on towel-dried hair. Watch visually up to 15 min.",
        "is_public": True,
        "user_index": 0
    },
    {
        "title": "Jessica T. - Cowboy Copper Gloss",
        "brand": "Redken",
        "shades": "07CC + 08CR + 06AA",
        "developer": "10 vol",
        "processing_time": 25,
        "notes": "Rich reflective auburn copper. 1:1 ratio. Scalp to ends for 25 minutes. Deep conditioning treatment immediately after rinse.",
        "is_public": True,
        "user_index": 0
    },
    {
        "title": "Ashley B. - Butter Blonde Balayage Gloss",
        "brand": "Redken",
        "shades": "09GI + 09GB + Clear",
        "developer": "10 vol",
        "processing_time": 20,
        "notes": "Soft golden cream tone over foil highlights. Equal parts 09GI and 09GB with splash of Clear to dilute tone.",
        "is_public": True,
        "user_index": 1
    },
    {
        "title": "Amanda L. - Mushroom Brown Gloss",
        "brand": "Redken",
        "shades": "06NA + 07T Steel",
        "developer": "10 vol",
        "processing_time": 20,
        "notes": "Neutralize warmth on faded level 6 brassy brunette. Cool earthy reflects without pulling green.",
        "is_public": True,
        "user_index": 1
    },
    {
        "title": "Olivia C. - Espresso Brunette Lowlights",
        "brand": "Redken",
        "shades": "04NCH + 05NW",
        "developer": "20 vol",
        "processing_time": 35,
        "notes": "Dimension addition on over-highlighted hair. Weave into foils, leave tips out for brightness.",
        "is_public": False,
        "user_index": 1
    },
    {
        "title": "Megan R. - Cherry Cola Gloss",
        "brand": "Redken",
        "shades": "05RV + 06RR + 04VRO",
        "developer": "10 vol",
        "processing_time": 25,
        "notes": "Vibrant violet red brunette tone. High gloss finish under direct indoor lighting.",
        "is_public": True,
        "user_index": 2
    },
    {
        "title": "Rachel D. - Smoky Ash Base Break",
        "brand": "Redken",
        "shades": "08AB + 09NA",
        "developer": "20 vol",
        "processing_time": 10,
        "notes": "Quick base bump during shampoo. 10 minutes maximum to soften level 6 natural regrowth between foils.",
        "is_public": False,
        "user_index": 2
    },
    {
        "title": "Chloe H. - Vanilla Cream Face Frame",
        "brand": "Redken",
        "shades": "010NW + 010GI + 09V",
        "developer": "10 vol",
        "processing_time": 20,
        "notes": "Money piece toning formula. Neutral warm balance. Applied last at the basin.",
        "is_public": True,
        "user_index": 2
    },
    {
        "title": "Brittany N. - Golden Peach Glaze",
        "brand": "Redken",
        "shades": "08WG + 09AA + 09GB",
        "developer": "10 vol",
        "processing_time": 20,
        "notes": "Spring seasonal glaze on pre-lightened level 8 hair. High shine, soft warmth.",
        "is_public": True,
        "user_index": 0
    },

    # ---- WELLA COLOR TOUCH & KOLESTON PERFECT ----
    {
        "title": "Hannah S. - Sandy Beige Blonde",
        "brand": "Wella",
        "shades": "9/97 + 9/16",
        "developer": "10 vol",
        "processing_time": 20,
        "notes": "Color Touch demi. 2:1 ratio with 1.9% emulsion (10 vol). Cool beige tone on level 9 highlights.",
        "is_public": True,
        "user_index": 0
    },
    {
        "title": "Samantha P. - Deep Chocolate Coverage",
        "brand": "Wella",
        "shades": "5/71 + 5/0 (1:1)",
        "developer": "20 vol",
        "processing_time": 35,
        "notes": "Koleston Perfect on 60% resistant grey hair. 1:1 with Welloxon 20 vol. Process full 35 minutes.",
        "is_public": False,
        "user_index": 0
    },
    {
        "title": "Taylor V. - Honey Glaze Gloss",
        "brand": "Wella",
        "shades": "8/73 + 8/38",
        "developer": "10 vol",
        "processing_time": 20,
        "notes": "Color Touch demi-permanent. Beautiful luminous warm honey reflects on virgin hair.",
        "is_public": True,
        "user_index": 1
    },
    {
        "title": "Lauren M. - Nordic Frost Toner",
        "brand": "Wella",
        "shades": "10/81 + 10/16 Special Blonde",
        "developer": "10 vol",
        "processing_time": 15,
        "notes": "Ultra cool pastel pearl blonde. Apply immediately following bleach wash. Rinse cool water.",
        "is_public": True,
        "user_index": 1
    },
    {
        "title": "Danielle K. - Autumn Ginger Melt",
        "brand": "Wella",
        "shades": "7/43 + 6/34 (Roots) / 8/41 (Ends)",
        "developer": "20 vol",
        "processing_time": 30,
        "notes": "Full transformation on natural level 6. Bright natural copper with golden undertones.",
        "is_public": True,
        "user_index": 1
    },
    {
        "title": "Nicole F. - Smokey Pearl Brunette",
        "brand": "Wella",
        "shades": "6/97 + 7/18",
        "developer": "10 vol",
        "processing_time": 25,
        "notes": "Illumina color line for sheer translucent finish. Perfect tone-down formula after summer sun.",
        "is_public": True,
        "user_index": 2
    },
    {
        "title": "Kaitlyn W. - Rich Chestnut Grey Blend",
        "brand": "Wella",
        "shades": "6/77 + 6/0",
        "developer": "20 vol",
        "processing_time": 40,
        "notes": "Resistant temples. Applied 6/0 first to hairline then cross-checked back quadrants.",
        "is_public": False,
        "user_index": 2
    },
    {
        "title": "Victoria G. - Strawberry Rose Champagne",
        "brand": "Wella",
        "shades": "9/43 + 10/05",
        "developer": "10 vol",
        "processing_time": 20,
        "notes": "Pastel strawberry blush. Gorgeous reflection in natural daylight. Customer loved it.",
        "is_public": True,
        "user_index": 2
    },
    {
        "title": "Sydney O. - Jet Velvet Brunette",
        "brand": "Wella",
        "shades": "3/0 + 4/71",
        "developer": "20 vol",
        "processing_time": 35,
        "notes": "Deep dark reflective espresso. Added Post Color Treatment for shine seal.",
        "is_public": True,
        "user_index": 0
    },
    {
        "title": "Alexis Z. - Warm Biscuit Babylights Toner",
        "brand": "Wella",
        "shades": "9/73 + 9/96",
        "developer": "5 vol",
        "processing_time": 15,
        "notes": "Subtle creamy beige. Keeps highlights bright without over-toning ashy.",
        "is_public": True,
        "user_index": 1
    },

    # ---- SCHWARZKOPF IGORA ROYAL & VIBRANCE ----
    {
        "title": "Maria E. - Raw Honey Balayage",
        "brand": "Schwarzkopf",
        "shades": "9.5-4 + 9-55 Raw Honey",
        "developer": "10 vol",
        "processing_time": 20,
        "notes": "Igora Vibrance tone-on-tone gel. Gel developer 1.9% 1:1. Incredible condition and gloss.",
        "is_public": True,
        "user_index": 0
    },
    {
        "title": "Elena R. - Cendre Silver Platinum",
        "brand": "Schwarzkopf",
        "shades": "9.5-1 + 9.5-21 Cendre",
        "developer": "10 vol",
        "processing_time": 15,
        "notes": "Anti-yellow formulation for level 10 bleached canvas. Apply root to ends smoothly.",
        "is_public": True,
        "user_index": 0
    },
    {
        "title": "Grace T. - Intense Copper Flame",
        "brand": "Schwarzkopf",
        "shades": "7-77 + 8-77 + 0-77 Booster",
        "developer": "20 vol",
        "processing_time": 35,
        "notes": "Igora Royal high-octane red copper. Added 2g of 0-77 tone booster for extra vibrancy.",
        "is_public": True,
        "user_index": 1
    },
    {
        "title": "Claire J. - Natural Warm Mocha",
        "brand": "Schwarzkopf",
        "shades": "6-46 + 6-0",
        "developer": "20 vol",
        "processing_time": 30,
        "notes": "Chocolate gold beige reflection. Natural coverage on fading ends.",
        "is_public": False,
        "user_index": 1
    },
    {
        "title": "Natalie M. - Dusty Rose Gold Toner",
        "brand": "Schwarzkopf",
        "shades": "9.5-49 + 0-00 Clear",
        "developer": "10 vol",
        "processing_time": 20,
        "notes": "Vibrance pastel toner. Clear dilution reduces intensity to soft blush.",
        "is_public": True,
        "user_index": 2
    },
    {
        "title": "Leah S. - Smoky Steel Brunette",
        "brand": "Schwarzkopf",
        "shades": "5-1 + 5-21 Cendre Ash",
        "developer": "20 vol",
        "processing_time": 30,
        "notes": "Counteract stubborn brass on level 5 hair. Cool reflective finish without hollow look.",
        "is_public": True,
        "user_index": 2
    },
    {
        "title": "Zoe D. - Dark Amethyst Gloss",
        "brand": "Schwarzkopf",
        "shades": "4-99 + 5-99 Violet Extra",
        "developer": "10 vol",
        "processing_time": 25,
        "notes": "Deep dark plum tone. Rich burgundy sheen under salon halogen lights.",
        "is_public": True,
        "user_index": 0
    },

    # ---- L'OREAL PROFESSIONNEL MAJIREL & DIA LIGHT ----
    {
        "title": "Sophia K. - French Gloss Bronde",
        "brand": "L'Oreal",
        "shades": "Dia Light 7.01 + 8.18",
        "developer": "10 vol",
        "processing_time": 20,
        "notes": "Acidic gloss formula. Zero lift, high shine on sensitized bleached mid-lengths.",
        "is_public": True,
        "user_index": 0
    },
    {
        "title": "Gabriella P. - Pearl Milkshake Toner",
        "brand": "L'Oreal",
        "shades": "Dia Light 10.12 + 10.21",
        "developer": "10 vol",
        "processing_time": 15,
        "notes": "Perfect iridescent pearl for babylight clients. Apply at basin, emulsify thoroughly.",
        "is_public": True,
        "user_index": 1
    },
    {
        "title": "Isabella V. - Deep Walnut Grey Touchup",
        "brand": "L'Oreal",
        "shades": "Majirel 5.0 + 5.35",
        "developer": "20 vol",
        "processing_time": 35,
        "notes": "Full opacity grey coverage. 1:1.5 mixing ratio with 20 volume cream developer.",
        "is_public": False,
        "user_index": 1
    },
    {
        "title": "Alyssa C. - Copper Caramel Gloss",
        "brand": "L'Oreal",
        "shades": "Dia Light 7.43 + 8.3",
        "developer": "10 vol",
        "processing_time": 20,
        "notes": "Warm caramel copper refresher between highlight appointments.",
        "is_public": True,
        "user_index": 2
    },
    {
        "title": "Camilla N. - Cool Ash Brunette Melt",
        "brand": "L'Oreal",
        "shades": "Majirel Cool Inforced 6.1 + 7.11",
        "developer": "20 vol",
        "processing_time": 35,
        "notes": "Intense anti-red reflection. Designed for resistant warm undertones.",
        "is_public": True,
        "user_index": 2
    },

    # ---- GOLDWELL TOPCHIC & COLORANCE ----
    {
        "title": "Hailey M. - Soft Beige Pearl Glow",
        "brand": "Goldwell",
        "shades": "Colorance 9-BA + 10-BS",
        "developer": "10 vol",
        "processing_time": 20,
        "notes": "Acidic demi-permanent toning. Silky cuticle restoration on bleached ribbons.",
        "is_public": True,
        "user_index": 0
    },
    {
        "title": "Audrey H. - Golden Pecan Root Shadow",
        "brand": "Goldwell",
        "shades": "Colorance 6-B + 7-N",
        "developer": "10 vol",
        "processing_time": 15,
        "notes": "Root tap technique with 6-B to soften contrast on high-lift blonde base.",
        "is_public": True,
        "user_index": 1
    },
    {
        "title": "Evelyn S. - Intense Fiery Copper",
        "brand": "Goldwell",
        "shades": "Topchic 7-RO + 8-OR",
        "developer": "30 vol",
        "processing_time": 35,
        "notes": "2 levels of lift on virgin level 5 hair. Gorgeous brilliant sunset copper.",
        "is_public": True,
        "user_index": 2
    },
    {
        "title": "Penelope W. - Velvet Blackberry",
        "brand": "Goldwell",
        "shades": "Colorance 4-VV + 5-V",
        "developer": "10 vol",
        "processing_time": 25,
        "notes": "Deep gothic violet tone. Leaves hair ultra reflective under studio lighting.",
        "is_public": False,
        "user_index": 0
    },

    # ---- MATRIX SOCOLOR & TONAL CONTROL ----
    {
        "title": "Brooke T. - Nude Rose Blonde",
        "brand": "Matrix",
        "shades": "Tonal Control 9NV + 10PR",
        "developer": "10 vol",
        "processing_time": 20,
        "notes": "Pre-bonded acidic gel toner. Visible oxidation indicator ensures reliable pull-timing.",
        "is_public": True,
        "user_index": 0
    },
    {
        "title": "Morgan E. - Rich Mocha Brunette",
        "brand": "Matrix",
        "shades": "SoColor 5M + 6MM Mocha",
        "developer": "20 vol",
        "processing_time": 35,
        "notes": "1:1 with 20 volume Matrix cream. Rich multi-dimensional chocolate coverage.",
        "is_public": True,
        "user_index": 1
    },
    {
        "title": "Vanessa L. - Ice Queen Double Process",
        "brand": "Matrix",
        "shades": "Tonal Control 11PA + 10AA",
        "developer": "10 vol",
        "processing_time": 20,
        "notes": "Strictly pale silver frost. No warm tones remaining.",
        "is_public": True,
        "user_index": 2
    },
    {
        "title": "Destiny K. - Spiced Cinnamon Melt",
        "brand": "Matrix",
        "shades": "SoColor 7CC + 7BC",
        "developer": "20 vol",
        "processing_time": 35,
        "notes": "Warm cinnamon copper with bronze depth. Great holiday season transformation.",
        "is_public": False,
        "user_index": 0
    },

    # ---- PULP RIOT SEMI-PERMANENT & LIQUID DEMI ----
    {
        "title": "Maya F. - Electric Neon Sunset",
        "brand": "Pulp Riot",
        "shades": "Pyro + Lava + Fireball",
        "developer": "5 vol",
        "processing_time": 30,
        "notes": "Direct semi-permanent on clean level 9 canvas. Feathered together for flame gradient.",
        "is_public": True,
        "user_index": 1
    },
    {
        "title": "Stella R. - Midnight Blue & Violet Melt",
        "brand": "Pulp Riot",
        "shades": "Nightfall + Velvet + Smoke",
        "developer": "5 vol",
        "processing_time": 30,
        "notes": "Deep jewel tones. Apply dry, saturating every strand. Cold water rinse only.",
        "is_public": True,
        "user_index": 2
    },
    {
        "title": "Ruby D. - Lilac Dream Pastel",
        "brand": "Pulp Riot",
        "shades": "Lilac + Powder + Clear",
        "developer": "5 vol",
        "processing_time": 25,
        "notes": "Diluted with 75% Clear for ethereal pastel lavender tones on level 10 platinum.",
        "is_public": True,
        "user_index": 0
    },
    {
        "title": "Ivy G. - Emerald Forest Split Dye",
        "brand": "Pulp Riot",
        "shades": "Absinthe + Nightfall + Noir",
        "developer": "5 vol",
        "processing_time": 35,
        "notes": "Deep dark forest green. Noir added at the root for shadow root effect.",
        "is_public": True,
        "user_index": 1
    },

    # ---- JOICO & KENRA PROFESSIONAL ----
    {
        "title": "Claire B. - Rose Gold Shimmer",
        "brand": "Joico",
        "shades": "LumiShine 9NVR + 10V",
        "developer": "5 vol",
        "processing_time": 15,
        "notes": "Argiplex bond-building demi liquid. High shine and gentle on sensitized hair.",
        "is_public": True,
        "user_index": 2
    },
    {
        "title": "Jenna M. - Silver Pearl Metallic",
        "brand": "Kenra",
        "shades": "Demi 9VM + 10SM Silver Metallic",
        "developer": "10 vol",
        "processing_time": 20,
        "notes": "Signature Kenra Metallic line. Requires level 10 yellow-free base for true silver cast.",
        "is_public": True,
        "user_index": 0
    },
    {
        "title": "Paige W. - Golden Apricot Blonde",
        "brand": "Joico",
        "shades": "LumiShine 8NC + 9NG",
        "developer": "10 vol",
        "processing_time": 20,
        "notes": "Soft apricot blonde. Gives hair healthy luminosity and warmth.",
        "is_public": True,
        "user_index": 1
    },
    {
        "title": "Sydney T. - Bronze Goddess Melt",
        "brand": "Kenra",
        "shades": "Demi 7B + 7BR Bronze",
        "developer": "10 vol",
        "processing_time": 25,
        "notes": "Warm reflective bronze melt on natural brown hair. Smooth gradient.",
        "is_public": True,
        "user_index": 2
    }
]

# Designated Seed Accounts
SEED_USERS = [
    {
        "username": "jane_stylist",
        "email": "jane@salonsync.com",
        "password": "StylistPassword2026!",
        "role": "member"
    },
    {
        "username": "carlos_color",
        "email": "carlos@salonsync.com",
        "password": "StylistPassword2026!",
        "role": "member"
    },
    {
        "username": "elena_balayage",
        "email": "elena@salonsync.com",
        "password": "StylistPassword2026!",
        "role": "member"
    },
    {
        "username": "moderator_admin",
        "email": "moderator@salonsync.com",
        "password": "ModPassword2026!",
        "role": "moderator"
    }
]


def seed_database():
    """Populates users and authentic formula notes idempotently."""
    users_created = 0
    users_existing = 0
    notes_created = 0

    user_objs = []
    for u_data in SEED_USERS:
        existing = User.query.filter_by(username=u_data["username"]).first()
        if not existing:
            user = User(
                username=u_data["username"],
                email=u_data["email"],
                role=u_data["role"]
            )
            user.set_password(u_data["password"])
            db.session.add(user)
            db.session.flush()
            user_objs.append(user)
            users_created += 1
        else:
            # Ensure role and password are set
            existing.role = u_data["role"]
            existing.set_password(u_data["password"])
            user_objs.append(existing)
            users_existing += 1

    # Base timestamp set to realistic recent days
    base_time = datetime.now(timezone.utc) - timedelta(days=14)

    # Multiply and curate formulas so the catalog features 150+ realistic formulations
    multiplier = 4  # 48 base formulas * 4 variations = 192 total notes
    stylist_users = [u for u in user_objs if u.role == "member"]

    note_counter = 0
    for round_idx in range(multiplier):
        for base_formula in SEED_FORMULAS:
            note_counter += 1
            client_id = f"Client #{note_counter:03d}"

            # Variant title
            variant_title = base_formula["title"]
            if round_idx > 0:
                variant_title = f"{base_formula['title']} (Refinement {round_idx + 1})"

            # Assign user in rotation among members
            user_target = stylist_users[(base_formula["user_index"] + round_idx) % len(stylist_users)]

            # Check if this exact title exists for this user
            existing_note = Note.query.filter_by(user_id=user_target.id, title=variant_title).first()
            if not existing_note:
                note_created_at = base_time + timedelta(hours=note_counter * 1.5)
                new_note = Note(
                    user_id=user_target.id,
                    title=variant_title,
                    brand=base_formula["brand"],
                    shades=base_formula["shades"],
                    developer=base_formula["developer"],
                    processing_time=base_formula["processing_time"],
                    notes=f"[{client_id}] {base_formula['notes']}",
                    is_public=base_formula["is_public"],
                    created_at=note_created_at,
                    updated_at=note_created_at
                )
                db.session.add(new_note)
                notes_created += 1

    db.session.commit()
    return {
        "users_created": users_created,
        "users_existing": users_existing,
        "notes_created": notes_created,
        "total_notes": Note.query.count(),
        "total_users": User.query.count()
    }


@click.command("seed")
@with_appcontext
def seed_command():
    """Seed the database with authentic salon formulas and demo accounts."""
    click.echo("Seeding SalonSync demonstration fixtures...")
    stats = seed_database()
    click.echo(
        f"Done! Users: {stats['users_created']} created, {stats['users_existing']} existing. "
        f"Notes: {stats['notes_created']} created (Total in DB: {stats['total_notes']})."
    )
