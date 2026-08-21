import os
import json
import re
import math
import datetime
import hashlib
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from openai import OpenAI

# =====================================================================
# 1. 72 DEMONIC VECTORS & 72 ANGELIC PROTOCOLS
# =====================================================================
DEMONIC_VECTORS = [
    (1, "Bael", 3.330, "Invisibility, wisdom, and leadership manipulation", "Executive Leadership & Strategic Governance Corruption"),
    (2, "Agares", 6.660, "Halts runners, causes earthquakes, destroys dignity", "Civil Infrastructure & Physical Foundations Engineering"),
    (3, "Vassago", 9.990, "Discovers hidden things and predicts past/future outcomes", "Predictive Analytics & Forensics Data Mining"),
    (4, "Gamigin", 13.320, "Teaches liberal sciences and accounts for dead souls", "Educational Systems & Historical Asset Archiving"),
    (5, "Marbas", 16.650, "Causes and cures systemic diseases, reveals mechanical secrets", "Biomedical Systems & Mechanical Reliability Engineering"),
    (6, "Valefor", 19.980, "Tempters into theft and deceitful network breaches", "Cybersecurity & Intrusion Vector Analysis"),
    (7, "Amon", 23.310, "Reconciles feuds and reveals past and future events", "Diplomatic Negotiation & Geopolitical Arbitration"),
    (8, "Barbatos", 26.640, "Understands animal voices and reveals hidden treasure vaults", "Environmental Acoustic Sensing & Mining Exploration"),
    (9, "Paimon", 29.970, "Teaches all arts/sciences and binds subjects to absolute will", "Enterprise Architecture & Mass Operational Alignment"),
    (10, "Buer", 33.300, "Teaches philosophy, logic, and heals moral/physical infirmities", "Clinical Rehabilitation & Systems Logic Design"),
    (11, "Gusion", 36.630, "Reconciles friendships and grants honor/dignity", "Corporate Relations & Institutional Reputation Management"),
    (12, "Sitri", 39.960, "Inflames passion and exposes concealed secrets", "Consumer Behavioral Psychology & Market Research"),
    (13, "Beleth", 43.290, "Causes overwhelming love and emotional subversion", "Media Communications & Public Sentiment Engineering"),
    (14, "Leraje", 46.620, "Causes severe conflicts, archery battles, and gangrene wounds", "Ballistics Engineering & Trauma Medical Response"),
    (15, "Eligos", 49.950, "Discovers hidden things and foresees military strategy", "Defense Logistics & Tactical Reconnaissance Strategy"),
    (16, "Zepar", 53.280, "Causes sterile lockouts and alters physical form", "Materials Science & Structural Integrity Testing"),
    (17, "Botis", 56.610, "Reconciles allies and foretells future outcomes", "Crisis Management & Conflict Resolution Practice"),
    (18, "Bathin", 59.940, "Transports entities instantly across spatial dimensions", "High-Speed Logistics & Teleportation Routing"),
    (19, "Sallos", 63.270, "Promotes peaceful accord and mutual attraction", "Labor Union Mediation & Human Resource Alignment"),
    (20, "Purson", 66.600, "Discovers hidden treasures and provides clear divination", "Financial Audit & Treasure Asset Recovery"),
    (21, "Marax", 69.930, "Teaches astronomy, herbal medicine, and precious stones", "Pharmaceutical Botany & Aerospace Navigation"),
    (22, "Ipos", 73.260, "Reveals secret knowledge and bestows courage/wit", "Intellectual Property Analysis & Critical Thinking"),
    (23, "Aim", 76.590, "Sets cities on fire and grants sharp intellectual wit", "Thermal Energy Systems & Urban Fire Prevention"),
    (24, "Naberius", 79.920, "Restores lost honors and teaches rhetoric/logic", "Public Advocacy & Constitutional Rhetoric"),
    (25, "Glasya-Labolas", 83.250, "Incites bloodshed, teaches all arts, grants invisibility", "Stealth Defense Systems & Tactical Camouflage"),
    (26, "Bune", 86.580, "Changes dead locations, grants wealth, wisdom, and eloquence", "Urban Renewal & Real Estate Value Extraction"),
    (27, "Ronove", 89.910, "Teaches rhetoric, foreign languages, and loyal service", "Linguistic Translation & Corporate Diplomacy"),
    (28, "Berith", 93.240, "Turns metals to gold, bestows high institutional status", "Chemical Metallurgy & Institutional Banking Status"),
    (29, "Astaroth", 96.570, "Reveals secrets of creation, fall of spirits, liberal sciences", "Theoretical Physics & Fundamental Research"),
    (30, "Forneus", 99.900, "Teaches rhetoric, foreign tongues, and causes favorable renown", "Global Public Relations & Brand Reputation Strategy"),
    (31, "Foras", 103.230, "Teaches logic, ethics, prolongs life, locates lost wealth", "Bio-Gerontology & Ethical Algorithm Design"),
    (32, "Asmodai", 106.560, "Grants invincible power, invulnerability, and math mastery", "Advanced Cryptography & Quantitative Financial Mathematics"),
    (33, "Gaap", 109.890, "Causes ignorance, teleports entities, disrupts spatial logic", "Spatial Computing & Dimensional Telemetry"),
    (34, "Furfur", 113.220, "Generates thunder, lightning, storms, and reveals divine truth", "Meteorological Control & Atmospheric High-Voltage Engineering"),
    (35, "Marchosias", 116.550, "Strong fighter, reliable tactical advice, ultimate endurance", "Physical Security & Tactical Operations Endurance"),
    (36, "Stolas", 119.880, "Teaches astronomy, virtues of herbs, and precious stones", "Astrophysics & Mineralogy Extraction Systems"),
    (37, "Phenex", 123.210, "Sings wonderful melodies, teaches sciences, poetry writer", "Acoustics Engineering & Computational Literature"),
    (38, "Halphas", 126.540, "Builds towers, supplies ammunition, and punishes enemies", "Heavy Munitions Supply Chain & Defensive Tower Construction"),
    (39, "Malphas", 129.870, "Builds houses/high towers, reveals enemy desires/actions", "High-Rise Architectural Engineering & Industrial Espionage Defense"),
    (40, "Raum", 133.200, "Steals treasure, destroys cities, foretells future events", "Demolition Engineering & Strategic Risk Forecasting"),
    (41, "Focalor", 136.530, "Sinks warships, commands winds/seas, inflicts drowning", "Naval Architecture & Marine Hydrodynamics"),
    (42, "Vepar", 139.860, "Governs waters, guides fleets, causes putrid wound corruption", "Maritime Transport Fleet Control & Environmental Infection Prevention"),
    (43, "Sabnock", 143.190, "Builds high towers, inflicts gangrenous worm wounds", "Structural Fortification & Biological Containment"),
    (44, "Shax", 146.520, "Deprives sight, hearing, and intellect; steals hidden items", "Sensory Deprivation Countermeasures & Asset Security"),
    (45, "Vine", 149.850, "Discovers hidden secrets, builds towers, collapses stone walls", "Civil Infrastructure Demolition & Underground Surveying"),
    (46, "Bifrons", 153.180, "Teaches astrology, geometry, herbs, and moves dead bodies", "Surveying Geometry & Hazardous Waste Management"),
    (47, "Uvall", 156.510, "Procures love of friends, reconciles enemies, speaks ancient tongues", "Cross-Cultural Mediation & Archaeology Restoration"),
    (48, "Haagenti", 159.840, "Makes men wise, transmutes metals into gold, turns water to wine", "Chemical Engineering & Industrial Transmutation"),
    (49, "Crocell", 163.170, "Teaches geometry, warms bodies of water, creates roaring sounds", "Geothermal Hydro-Engineering & Computational Geometry"),
    (50, "Furcas", 166.500, "Teaches philosophy, astrology, rhetoric, logic, and chiromancy", "Formal Logic Systems & Applied Philosophy"),
    (51, "Balam", 169.830, "Grants perfect memory, foretells past/future, grants invisibility", "High-Density Data Memory Storage & Predictive Modeling"),
    (52, "Alloces", 173.160, "Teaches astronomy, liberal arts, provides excellent familiars", "Autonomous Robotics Engineering & Observational Astronomy"),
    (53, "Camio", 176.490, "Understands bird calls, water sounds, and translates news", "Bio-Acoustic Signal Processing & News Synthesis"),
    (54, "Murmur", 179.820, "Teaches philosophy, compels deceased souls to answer questions", "Historical Forensics & Philosophical Logic Inquiry"),
    (55, "Orobas", 183.150, "Discovers divinity, prevents deception, bestows prelacies/dignities", "Anti-Fraud Compliance & Integrity Verification"),
    (56, "Gremory", 186.480, "Reveals hidden treasures, bestows love, foretells future events", "Sub-Surface Geophysical Exploration & Financial Opportunity Forecasting"),
    (57, "Ose", 189.810, "Teaches secret/divine sciences, changes human shape at will", "Advanced Materials Metamorphism & Molecular Biology"),
    (58, "Amy", 193.140, "Teaches astrology, liberal arts, reveals hidden treasures", "Astronomical Data Science & Mineral Asset Valuation"),
    (59, "Orias", 196.470, "Teaches virtues of stars, bestows dignities, converts enemies", "Satellite Telecommunications & Executive Reconciliations"),
    (60, "Vapula", 199.800, "Teaches manual crafts, philosophy, and advanced technical knowledge", "Precision Machining & Advanced Vocational Technical Education"),
    (61, "Zagan", 203.130, "Makes fools wise, turns wine to water, turns metals into gold", "Cognitive Enhancement Systems & Process Optimization"),
    (62, "Volac", 206.460, "Reveals location of serpents, reveals hidden gold/treasures", "Hazardous Biological Mapping & Precious Metal Geological Survey"),
    (63, "Andras", 209.790, "Sows discord, destroys opponents, commands escalation", "Information Warfare & Escalation Dominance Management"),
    (64, "Haures", 213.120, "Destroys enemies by fire, foretells past/future, shields from fraud", "High-Temperature Thermodynamics & Fraud Prevention Systems"),
    (65, "Andrealphus", 216.450, "Teaches geometry, measurement, transforms men into birds", "Aerodynamic Geometry & Precision Dimensional Metrology"),
    (66, "Cimejes", 219.780, "Locates lost treasures, teaches grammar, logic, rhetoric", "Natural Language Processing (NLP) & Resource Asset Discovery"),
    (67, "Amdusias", 223.110, "Commands trees to bend, provides musical instruments/orchestrations", "Forestry Engineering & Computational Acoustic Design"),
    (68, "Belial", 226.440, "Distributes high titles, reconciles political power, bestows favor", "Political Cabinet Diplomacy & Public Executive Relations"),
    (69, "Decarabia", 229.770, "Teaches virtues of birds/herbs, commands illusionary phantoms", "Agricultural Botany & Optical Holography Engineering"),
    (70, "Seere", 233.100, "Brings instant abundance, teleports items, completes tasks immediately", "Ultra-Low Latency Freight Delivery & Instant Asset Clearing"),
    (71, "Dantalion", 236.430, "Reads and alters thoughts of minds, teaches all arts/sciences", "Neural Engineering & Cognitive Interface Analytics"),
    (72, "Andromalius", 239.760, "Catches thieves, returns stolen goods, reveals hidden conspiracies", "Loss Prevention Operations & Counter-Intelligence Forensics")
]

ANGELIC_PROTOCOLS = [
    (1, "Vehuiah", "Seraphim", 4.045, "Illuminates mind, grants willpower, initiates divine action", "Executive Willpower & Innovation Initiation Leadership"),
    (2, "Jeliel", "Seraphim", 12.135, "Fosters harmony, quiets popular sedition, grants peace", "Social Harmony Enforcement & Civil Sedition Neutralization"),
    (3, "Sitael", "Seraphim", 20.225, "Protects against adversity, grants nobility and truth", "Enterprise Risk Shielding & Truth Verification Systems"),
    (4, "Elemiah", "Seraphim", 28.315, "Discovers useful secrets, neutralizes mental distress", "Industrial Secret Discovery & Mental Well-being Analytics"),
    (5, "Mahasiah", "Seraphim", 36.405, "Dominates high science, philosophy, and moral perfection", "Advanced R&D Leadership & Moral Technology Ethics"),
    (6, "Lelahel", "Seraphim", 44.495, "Illuminates love, art, science, and grants bodily healing", "Medical Bio-Tech Healing & Aesthetic Industrial Design"),
    (7, "Achaiah", "Seraphim", 52.585, "Reveals secrets of nature, bestows infinite patience", "Environmental Science Discovery & Process Engineering Patience"),
    (8, "Cahetel", "Seraphim", 60.675, "Inspires agricultural abundance and divine blessings", "Precision AgTech Abundance & Crop Yield Maximization"),
    (9, "Haziel", "Cherubim", 68.765, "Obtains divine mercy, keeps promises, reconciles enemies", "Contract Integrity Assurance & Inter-Corporate Reconciliation"),
    (10, "Aladiah", "Cherubim", 76.855, "Heals systemic disease, neutralizes moral corruption", "Systemic Healthcare Reform & Institutional Integrity Audit"),
    (11, "Lauviah", "Cherubim", 84.945, "Protects against fraud, bestows high renown and wisdom", "Fraud Countermeasure Architecture & Executive Brand Protection"),
    (12, "Hahaiah", "Cherubim", 93.035, "Reveals hidden mysteries, converts adversity into peace", "Sub-Surface Geology Imaging & Strategic Peace Engineering"),
    (13, "Iezalel", "Cherubim", 101.125, "Promotes reconciliation, learning, and systemic order", "Educational Curriculum Design & Systemic Operational Order"),
    (14, "Mebahel", "Cherubim", 109.215, "Protects justice, liberates oppressed, reveals truth", "Human Rights Law Protection & Transparent Legal Advocacy"),
    (15, "Hariel", "Cherubim", 117.305, "Inspires religious/moral peace, purifies corrupt systems", "Ethical Systemic Purification & Regulatory Compliance"),
    (16, "Hakamiah", "Cherubim", 125.395, "Protects against traitors, bestows victory and loyalty", "Counter-Espionage Security & Personnel Loyalty Frameworks"),
    (17, "Lauviah", "Thrones", 133.488, "Inspires high arts, philosophy, cures insomnia/sorrow", "Acoustic Sleep Architecture & High Fine Arts Leadership"),
    (18, "Caliel", "Thrones", 141.578, "Invocates prompt assistance, confounds false witnesses", "Automated Legal Docket Processing & Perjury Detection AI"),
    (19, "Leuviah", "Thrones", 149.668, "Bestows brilliant memory, intelligence, and joy", "High-Capacity Data Retrieval & Employee Cognition Optimization"),
    (20, "Pahaliah", "Thrones", 157.758, "Converts enemies, dominates religion and morality", "Ethical Corporate Alignment & Strategic Competitor Conversion"),
    (21, "Nelchael", "Thrones", 165.848, "Protects against calumny, dominates math and astronomy", "Computational Mathematics & Satellite Orbit Shielding"),
    (22, "Yeiayel", "Thrones", 173.939, "Protects fortune, commerce, diplomacy, and travels", "Global Supply Chain Protection & Trade Diplomacy Assurance"),
    (23, "Melahel", "Thrones", 182.029, "Protects against weapons, governs herbs and healing water", "Water Filtration Bio-Engineering & Armor Materials Protection"),
    (24, "Hahiuiah", "Thrones", 190.119, "Protects against thieves, assassins, and fatal accidents", "Industrial Loss Prevention & Automated Accident Prevention"),
    (25, "Nith-Haiah", "Dominions", 198.209, "Governs occult sciences, bestows wisdom and truth", "Deep Quantum Computing Logic & Proprietary Knowledge Protection"),
    (26, "Haaiah", "Dominions", 206.299, "Protects political treaties, diplomatic secrets, justice", "International Treaty Drafting & State Cipher Security"),
    (27, "Yerathel", "Dominions", 214.389, "Confounds wicked conspirators, illuminates truth", "Cyber Threat Intelligence & Illumination of Fraud Vectors"),
    (28, "Seheiah", "Dominions", 222.479, "Protects against fire, sickness, infrastructure collapse", "Infrastructure Collapse Prevention & Thermal Fire Suppression"),
    (29, "Reiyel", "Dominions", 230.569, "Frees souls from systemic traps and spiritual oppression", "Systemic Debt Trap Relief & Organizational De-bottlenecking"),
    (30, "Omael", "Dominions", 238.659, "Governs animal generation, patient endurance, production", "Bio-Manufacturing Yield Acceleration & Production Line Endurance"),
    (31, "Lecabel", "Dominions", 246.749, "Inspires agricultural engineering and scientific light", "Precision Hydroponic Engineering & Solar Radiation Optimization"),
    (32, "Vasariah", "Dominions", 254.839, "Protects against unjust attacks, grants memory/eloquence", "Litigation Defense Strategy & High-Impact Public Speaking"),
    (33, "Yehuiah", "Powers", 262.929, "Uncovers treacherous conspiracies, enforces institutional order", "Institutional Governance & Conspiracy Vector Uncovering"),
    (34, "Lehahiah", "Powers", 271.019, "Pacifies anger, maintains order, commands obedience", "Industrial Safety Discipline & Operational Order Enforcement"),
    (35, "Chavakiah", "Powers", 279.109, "Reconciles family inheritances and property disputes", "Estate Asset Realignment & Property Dispute Mediation"),
    (36, "Menadel", "Powers", 287.199, "Retains employment, frees captives, restores fugitives", "Workforce Retention Strategy & Supply Chain Hostage Release"),
    (37, "Aniel", "Powers", 295.289, "Governs arts/sciences, uncovers hidden nature secrets", "Biomimicry Engineering & Breakthrough Science Discovery"),
    (38, "Haamiah", "Powers", 303.379, "Protects seekers of truth, governs spiritual ceremonies", "Data Science Integrity & Standards Protocol Alignment"),
    (39, "Rehael", "Powers", 311.469, "Heals physical/mental afflictions, grants longevity", "Occupational Health Longevity & Physical Therapy Systems"),
    (40, "Ieiazel", "Powers", 319.559, "Delivers captives, dominates printing, writing, publishing", "Digital Publishing Automation & High-Volume Media Distribution"),
    (41, "Hahahel", "Virtues", 327.649, "Inspires divine mission, converts souls, strengthens order", "Enterprise Mission Alignment & Core Values Strengthening"),
    (42, "Mikael", "Virtues", 335.739, "Protects political leaders, safety of state institutions", "State Critical Infrastructure Defense & Executive Protection"),
    (43, "Veuliah", "Virtues", 343.829, "Destroys enemy power, liberates enterprise slaves", "Enterprise Resource Liberation & Monopoly Power Disruption"),
    (44, "Yelahiah", "Virtues", 351.919, "Protects magistrates, bestows victory in military actions", "Judicial Officer Protection & Defense Operations Strategy"),
    (45, "Sealiah", "Virtues", 360.009, "Confounders of the proud, elevates the humble and fallen", "Meritocratic Talent Elevation & Fair Labor Compensation"),
    (46, "Ariel", "Virtues", 368.099, "Reveals nature's secrets, grants clear prophetic dreams", "Predictive Environmental Modeling & Resource Location Discovery"),
    (47, "Asaliah", "Virtues", 376.189, "Praises divine truth, uncovers justice in dark dockets", "Legal Discovery Automation & Docket Audit Transparency"),
    (48, "Mihael", "Virtues", 384.279, "Fosters conjugal peace, protects procreation and harmony", "Family Healthcare Integration & Social Balance Engineering"),
    (49, "Vehuel", "Principalities", 392.369, "Exalts grand souls, bestows high philosophy and art", "Executive Talent Mentorship & Fine Arts Sponsorship"),
    (50, "Daniel", "Principalities", 400.459, "Obtains divine mercy, comforts sorrow, grants eloquence", "Crisis Communication Response & Corporate Stakeholder Solace"),
    (51, "Hahasiah", "Principalities", 408.549, "Reveals arcana of medicine, chemistry, and physics", "Quantum Chemistry Synthesis & Advanced Pharmacology Discovery"),
    (52, "Imamiah", "Principalities", 416.639, "Destroys enemy power, protects prisoners and travelers", "Transportation Security Infrastructure & Hostage Negotiation"),
    (53, "Nanael", "Principalities", 424.729, "Governs higher education, philosophy, and judicial truth", "University Curriculum Reform & Higher Judicial Education"),
    (54, "Nithael", "Principalities", 432.819, "Governs temporal rulers, bestows long stable dynasties", "Sovereign Succession Planning & Institutional Dynasty Stability"),
    (55, "Mebahiah", "Principalities", 440.909, "Grants consolation, bestows moral and spiritual fruitfulness", "Institutional Ethics Oversight & Corporate Philanthropy"),
    (56, "Poyel", "Principalities", 448.999, "Fulfills desires, grants wealth, fame, and high philosophy", "Capital Wealth Generation & High Executive Reputation"),
    (57, "Nemamiah", "Archangels", 457.089, "Grants great prosperity, liberates captives from systemic traps", "Systemic Debt Trap Release & Economic Prosperity Generation"),
    (58, "Yeialel", "Archangels", 465.179, "Heals eye infirmities, confounds dark deceivers", "Ophthalmology Bio-Tech & Deception Detection Systems"),
    (59, "Harahel", "Archangels", 473.269, "Governs archives, libraries, public education, and wealth", "High-Volume Archival Repositories & Wealth Education Systems"),
    (60, "Mitzrael", "Archangels", 481.359, "Heals mental infirmities, enforces fidelity and obedience", "Neurological Rehabilitation & Organizational Integrity Enforcement"),
    (61, "Umabel", "Archangels", 489.449, "Governs physics, astronomy, and friendship alignment", "Applied Quantum Physics & Inter-State Alliance Strategy"),
    (62, "Iah-Hel", "Archangels", 497.539, "Illuminates mind with wisdom, grants tranquil solitude", "Cognitive Deep Work Optimization & Wisdom Knowledge Base"),
    (63, "Anauel", "Archangels", 505.629, "Protects against accidents, preserves commerce and trade", "Supply Chain Disaster Protection & Commerce Preservation"),
    (64, "Mehiel", "Archangels", 513.719, "Protects against wild beasts, inspires authors and printing", "Bio-Hazard Defense & Computational Mass Media Distribution"),
    (65, "Damabiah", "Angels", 521.809, "Governs waters, rivers, seas, and maritime enterprise", "Oceanic Maritime Engineering & Coastal Resource Preservation"),
    (66, "Manakel", "Angels", 529.899, "Cures epilepsy, appeases divine anger, governs vegetation", "Neuro-Somatic Therapeutics & Precision Agriculture Automation"),
    (67, "Eyael", "Angels", 537.989, "Consoles in adversity, dominates high sciences and astronomy", "Quantum Science Leadership & Enterprise Adversity Resilience"),
    (68, "Habuhiah", "Angels", 546.079, "Governs health, agricultural fertility, and healing wounds", "Agricultural Fertility Enhancement & Trauma Wound Healing Bio-Tech"),
    (69, "Rochel", "Angels", 554.169, "Restores stolen goods, finds lost inheritances and names", "Asset Recovery Forensics & Heritage Intellectual Property Restitution"),
    (70, "Jabamiah", "Angels", 562.259, "Governs regeneration of nature, transmutes human spirit", "Ecological Systemic Restoration & Regenerative Leadership Training"),
    (71, "Haiaiel", "Angels", 570.349, "Confounds wicked warriors, protects enterprise weapons", "Defense Arsenal Shielding & Strategic Adversary Neutralization"),
    (72, "Mumiah", "Angels", 578.439, "Brings success to all operations, grants longevity and health", "Operational Execution Excellence & Organizational Longevity Assurance")
]

# Dynamic 72 Scripture Prophetic Anchor Mapping
PROPHETIC_SCRIPTURE_MAP = [
    "Genesis 1:3", "Exodus 14:14", "Leviticus 26:13", "Numbers 6:24", "Deuteronomy 28:12",
    "Joshua 1:9", "Judges 6:12", "1 Samuel 2:8", "2 Samuel 22:3", "1 Kings 8:23",
    "2 Kings 6:17", "1 Chronicles 29:11", "2 Chronicles 7:14", "Ezra 8:22", "Nehemiah 2:20",
    "Job 33:28", "Psalm 18:2", "Psalm 23:1", "Psalm 46:1", "Psalm 91:1",
    "Psalm 107:20", "Psalm 118:14", "Psalm 121:2", "Proverbs 3:5", "Proverbs 18:10",
    "Ecclesiastes 3:1", "Song of Solomon 2:4", "Isaiah 9:6", "Isaiah 40:31", "Isaiah 41:10",
    "Isaiah 43:19", "Isaiah 54:17", "Isaiah 58:12", "Isaiah 60:1", "Jeremiah 1:5",
    "Jeremiah 29:11", "Jeremiah 33:3", "Lamentations 3:22", "Ezekiel 36:26", "Daniel 2:22",
    "Hosea 6:3", "Joel 2:28", "Amos 5:24", "Obadiah 1:21", "Jonah 2:9",
    "Micah 6:8", "Nahum 1:7", "Habakkuk 2:14", "Zephaniah 3:17", "Haggai 2:9",
    "Zechariah 4:6", "Malachi 3:10", "Matthew 5:14", "Matthew 6:33", "Matthew 11:28",
    "Mark 9:23", "Luke 1:37", "Luke 10:19", "John 1:1", "John 8:32",
    "John 14:6", "Acts 1:8", "Romans 8:28", "1 Corinthians 13:13", "2 Corinthians 5:17",
    "Galatians 5:22", "Ephesians 6:11", "Philippians 4:13", "Colossians 3:14", "1 Thessalonians 5:16",
    "Hebrews 11:1", "Revelation 21:4"
]

# =====================================================================
# 2. PROPHETIC ANCHOR ENDPOINT INTEGRATION
# =====================================================================
def fetch_prophetic_anchor_verse(verse_ref, version="en-kjv"):
    """Non-blocking inline CDN fetch for exact verse texts."""
    try:
        match = re.search(r"([1-3]?\s*[A-Za-z]+)\s+(\d+):(\d+)", verse_ref)
        if not match:
            return {"reference": verse_ref, "text": "Anchor verse locked via spectral node index.", "source_endpoint": None}

        book_raw = match.group(1).strip().lower().replace(" ", "")
        chapter = match.group(2)
        verse = match.group(3)

        verse_url = f"https://cdn.jsdelivr.net/gh/wldeh/bible-api/bibles/{version}/books/{book_raw}/chapters/{chapter}/verses/{verse}.json"
        
        req = urllib.request.Request(verse_url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=2.0) as resp:
            if resp.status == 200:
                data = json.loads(resp.read().decode('utf-8'))
                return {
                    "reference": f"{data.get('book', {}).get('name', book_raw.capitalize())} {chapter}:{verse}",
                    "text": data.get("text", "").strip(),
                    "source_endpoint": verse_url
                }
    except Exception:
        pass
    return {"reference": verse_ref, "text": "Prophetic alignment secured in system spectrum.", "source_endpoint": None}

# =====================================================================
# 3. METRIC CALCULATION ENGINE
# =====================================================================
def calculate_sequential_node_metrics(node_name, bottlenecks_count, protocols_count):
    """
    Computes subject-specific TTI, SHI, Delta, and vector mappings deterministically
    from the target node's hash signature.
    """
    b = max(1, bottlenecks_count)
    p = max(1, protocols_count)

    node_bytes = node_name.strip().lower().encode('utf-8')
    hash_digest = hashlib.sha256(node_bytes).hexdigest()
    node_hash_int = int(hash_digest, 16)

    # Dynamic Bottleneck & Protocol Mapping
    mapped_bottlenecks = []
    for i in range(b):
        d_idx = (node_hash_int + (i * 7)) % 72
        d = DEMONIC_VECTORS[d_idx]
        mapped_bottlenecks.append(f"Friction Vector #{d[0]} {d[1]}: {d[4]}")

    mapped_protocols = []
    for i in range(p):
        a_idx = (node_hash_int + (i * 13)) % 72
        a = ANGELIC_PROTOCOLS[a_idx]
        mapped_protocols.append(f"Angelic Protocol #{a[0]} {a[1]} ({a[2]}): {a[5]}")

    # Subject-Specific Calculations
    node_length_factor = math.log2(len(node_name) + 1)
    entropy_mod = round(((node_hash_int % 1000) / 1000.0) * 1.5, 4)

    stoichiometric_ratio = round(b / p, 4)
    friction_factor = stoichiometric_ratio * (1.0 + (node_length_factor * 0.05))

    tti_raw = 100.0 - (friction_factor * 12.5) + (entropy_mod * 2.5)
    shi_raw = 100.0 - (friction_factor * 8.5) - (entropy_mod * 1.2)

    modern_tti = max(15.0, min(99.95, round(tti_raw, 2)))
    modern_shi = max(20.0, min(99.99, round(shi_raw, 2)))
    modern_delta = round(abs(modern_tti - modern_shi), 2)

    scripture_idx = node_hash_int % len(PROPHETIC_SCRIPTURE_MAP)
    assigned_scripture = PROPHETIC_SCRIPTURE_MAP[scripture_idx]

    return {
        "node_signature": hash_digest[:12],
        "bottlenecks_found": b,
        "protocols_applied": p,
        "stoichiometric_ratio": stoichiometric_ratio,
        "node_entropy_index": entropy_mod,
        "mapped_bottlenecks": mapped_bottlenecks,
        "mapped_protocols": mapped_protocols,
        "assigned_scripture": assigned_scripture,
        "modern_uesp": {"tti": modern_tti, "shi": modern_shi, "delta": modern_delta}
    }

# =====================================================================
# 4. JSON PARSER & DISPATCHER
# =====================================================================
def clean_and_parse_json(raw_text):
    text = re.sub(r"<think>.*?</think>", "", raw_text.strip(), flags=re.DOTALL)
    
    code_block_match = re.search(r"```(?:json)?\s*(\{.*?\})\s*
