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
# 1. THE 72 DEMONIC VECTORS (GOETIA SPECTRUM & HISTORICAL PARALLELS)
# =====================================================================
DEMONIC_VECTORS = [
    (1, "Bael", 3.330, "Invisibility, wisdom, and leadership manipulation", "Executive Leadership & Strategic Governance Corruption", "The Justinianic Court Intrigues and Imperial Bureaucracy (528-565 AD)"),
    (2, "Agares", 6.660, "Halts runners, causes earthquakes, destroys dignity", "Civil Infrastructure & Physical Foundations Engineering", "The Great Antioch Earthquake and Structural Reconstruction (526 AD)"),
    (3, "Vassago", 9.990, "Discovers hidden things and predicts past/future outcomes", "Predictive Analytics & Forensics Data Mining", "The Carolingian State Census and Fiscal Assessment Era (800-814 AD)"),
    (4, "Gamigin", 13.320, "Teaches liberal sciences and accounts for dead souls", "Educational Systems & Historical Asset Archiving", "The monastic scriptorium and Scholastic Asset Preservation Era (900-1100 AD)"),
    (5, "Marbas", 16.650, "Causes and cures systemic diseases, reveals mechanical secrets", "Biomedical Systems & Mechanical Reliability Engineering", "The Black Death Quarantine and Sanitary Reform Era (1347-1351 AD)"),
    (6, "Valefor", 19.980, "Tempters into theft and deceitful network breaches", "Cybersecurity & Intrusion Vector Analysis", "The Great Mint Debasement and Treasury Breach Era (1340-1360 AD)"),
    (7, "Amon", 23.310, "Reconciles feuds and reveals past and future events", "Diplomatic Negotiation & Geopolitical Arbitration", "The Treaty of Verdun and Carolingian Statecraft Arbitration (843 AD)"),
    (8, "Barbatos", 26.640, "Understands animal voices and reveals hidden treasure vaults", "Environmental Acoustic Sensing & Mining Exploration", "The Witwatersrand Deep-Level Mining Grid & Reef Survey Era (1886-1936 AD)"),
    (9, "Paimon", 29.970, "Teaches all arts/sciences and binds subjects to absolute will", "Enterprise Architecture & Mass Operational Alignment", "The Cathedral Construction Guild Standardization Era (1140-1250 AD)"),
    (10, "Buer", 33.300, "Teaches philosophy, logic, and heals moral/physical infirmities", "Clinical Rehabilitation & Systems Logic Design", "The University of Bologna Scholastic Logic and Legal Codification Era (1088 AD)"),
    (11, "Gusion", 36.630, "Reconciles friendships and grants honor/dignity", "Corporate Relations & Institutional Reputation Management", "The Hanseatic League Commercial Alliance and Diplomatic Era (1350-1650 AD)"),
    (12, "Sitri", 39.960, "Inflames passion and exposes concealed secrets", "Consumer Behavioral Psychology & Market Research", "The Venetian Rialto Merchant Agora and Market Intelligence Era (1400-1500 AD)"),
    (13, "Beleth", 43.290, "Causes overwhelming love and emotional subversion", "Media Communications & Public Sentiment Engineering", "The Gutenberg Press Information Revolution and Propaganda Era (1440-1500 AD)"),
    (14, "Leraje", 46.620, "Causes severe conflicts, archery battles, and gangrene wounds", "Ballistics Engineering & Trauma Medical Response", "The Battle of Agincourt Longbow Ballistics and Field Surgery Era (1415 AD)"),
    (15, "Eligos", 49.950, "Discovers hidden things and foresees military strategy", "Defense Logistics & Tactical Reconnaissance Strategy", "The Venetian Arsenal Naval Intelligence and Reconnaissance Era (1104-1500 AD)"),
    (16, "Zepar", 53.280, "Causes sterile lockouts and alters physical form", "Materials Science & Structural Integrity Testing", "The Toledo Steel Metallurgy and Sword Forging Inspection Era (1000-1600 AD)"),
    (17, "Botis", 56.610, "Reconciles allies and foretells future outcomes", "Crisis Management & Conflict Resolution Practice", "The Peace of Westphalia Sovereign State Settlement Era (1648 AD)"),
    (18, "Bathin", 59.940, "Transports entities instantly across spatial dimensions", "High-Speed Logistics & Teleportation Routing", "The Age of Discovery Transoceanic Maritime Logistics Era (1492-1650 AD)"),
    (19, "Sallos", 63.270, "Promotes peaceful accord and mutual attraction", "Labor Union Mediation & Human Resource Alignment", "The Florentine Wool Guild Labor Mediation Era (1378 AD)"),
    (20, "Purson", 66.600, "Discovers hidden treasures and provides clear divination", "Financial Audit & Treasure Asset Recovery", "The Spanish Treasure Fleet Auditing and Royal Exchequer Era (1550-1700 AD)"),
    (21, "Marax", 69.930, "Teaches astronomy, herbal medicine, and precious stones", "Pharmaceutical Botany & Aerospace Navigation", "The Copernican Astronomical Revolution and Botanical Indexing Era (1543 AD)"),
    (22, "Ipos", 73.260, "Reveals secret knowledge and bestows courage/wit", "Intellectual Property Analysis & Critical Thinking", "The Renaissance Florentine Academy and Intellectual Awakening Era (1450-1600 AD)"),
    (23, "Aim", 76.590, "Sets cities on fire and grants sharp intellectual wit", "Thermal Energy Systems & Urban Fire Prevention", "The Great Fire of London and Urban Building Code Era (1666 AD)"),
    (24, "Naberius", 79.920, "Restores lost honors and teaches rhetoric/logic", "Public Advocacy & Constitutional Rhetoric", "The Enlightenment Parliamentary Debate and Rhetoric Era (1750-1789 AD)"),
    (25, "Glasya-Labolas", 83.250, "Incites bloodshed, teaches all arts, grants invisibility", "Stealth Defense Systems & Tactical Camouflage", "The Napoleonic Reconnaissance and Infiltration Tactics Era (1804-1815 AD)"),
    (26, "Bune", 86.580, "Changes dead locations, grants wealth, wisdom, and eloquence", "Urban Renewal & Real Estate Value Extraction", "The Haussmann Renovation of Paris and Urban Renewal Era (1853-1870 AD)"),
    (27, "Ronove", 89.910, "Teaches rhetoric, foreign languages, and loyal service", "Linguistic Translation & Corporate Diplomacy", "The Rosetta Stone Decipherment and Diplomatic Translation Era (1822 AD)"),
    (28, "Berith", 93.240, "Turns metals to gold, bestows high institutional status", "Chemical Metallurgy & Institutional Banking Status", "The Industrial Gold Standard and Central Banking Era (1816-1914 AD)"),
    (29, "Astaroth", 96.570, "Reveals secrets of creation, fall of spirits, liberal sciences", "Theoretical Physics & Fundamental Research", "The Maxwellian Electrodynamics and Fundamental Physics Era (1865 AD)"),
    (30, "Forneus", 99.900, "Teaches rhetoric, foreign tongues, and causes favorable renown", "Global Public Relations & Brand Reputation Strategy", "The Victorian Global Exposition and Public Diplomacy Era (1851-1900 AD)"),
    (31, "Foras", 103.230, "Teaches logic, ethics, prolongs life, locates lost wealth", "Bio-Gerontology & Ethical Algorithm Design", "The Pasteur Germ Theory and Public Health Longevity Era (1860-1895 AD)"),
    (32, "Asmodai", 106.560, "Grants invincible power, invulnerability, and math mastery", "Advanced Cryptography & Quantitative Financial Mathematics", "The Enigma Codebreaking and Mathematical Cryptography Era (1939-1945 AD)"),
    (33, "Gaap", 109.890, "Causes ignorance, teleports entities, disrupts spatial logic", "Spatial Computing & Dimensional Telemetry", "The Early Aviation Radar and Spatial Mapping Era (1935-1950 AD)"),
    (34, "Furfur", 113.220, "Generates thunder, lightning, storms, and reveals divine truth", "Meteorological Control & Atmospheric High-Voltage Engineering", "The Tesla High-Voltage Electrical Transmission Era (1890-1910 AD)"),
    (35, "Marchosias", 116.550, "Strong fighter, reliable tactical advice, ultimate endurance", "Physical Security & Tactical Operations Endurance", "The Battle of Stalingrad Siege Resilience and Industrial Endurance (1942-1943 AD)"),
    (36, "Stolas", 119.880, "Teaches astronomy, virtues of herbs, and precious stones", "Astrophysics & Mineralogy Extraction Systems", "The Post-War Deep Geological Survey and Mineral Extraction Era (1945-1970 AD)"),
    (37, "Phenex", 123.210, "Sings wonderful melodies, teaches sciences, poetry writer", "Acoustics Engineering & Computational Literature", "The Bell Labs Acoustic Waveform and Computational Speech Era (1950-1975 AD)"),
    (38, "Halphas", 126.540, "Builds towers, supplies ammunition, and punishes enemies", "Heavy Munitions Supply Chain & Defensive Tower Construction", "The Cold War ICBM Silo Infrastructure and Logistics Era (1950-1980 AD)"),
    (39, "Malphas", 129.870, "Builds houses/high towers, reveals enemy desires/actions", "High-Rise Architectural Engineering & Industrial Espionage Defense", "The Post-War Skyscraper Boom and Corporate Espionage Defense Era (1950-1985 AD)"),
    (40, "Raum", 133.200, "Steals treasure, destroys cities, foretells future events", "Demolition Engineering & Strategic Risk Forecasting", "The Post-Industrial Urban Redevelopment and Demolition Era (1960-1990 AD)"),
    (41, "Focalor", 136.530, "Sinks warships, commands winds/seas, inflicts drowning", "Naval Architecture & Marine Hydrodynamics", "The Cold War Nuclear Submarine and Hydrodynamic Design Era (1955-1985 AD)"),
    (42, "Vepar", 139.860, "Governs waters, guides fleets, causes putrid wound corruption", "Maritime Transport Fleet Control & Environmental Infection Prevention", "The Containerization Shipping Revolution and Port Hygiene Era (1956-1980 AD)"),
    (43, "Sabnock", 143.190, "Builds high towers, inflicts gangrenous worm wounds", "Structural Fortification & Biological Containment", "The Cold War Civil Defense Fallout Shelter Engineering Era (1960-1985 AD)"),
    (44, "Shax", 146.520, "Deprives sight, hearing, and intellect; steals hidden items", "Sensory Deprivation Countermeasures & Asset Security", "The Intelligence Agency Electronic Surveillance and Counter-Sigint Era (1960-1990 AD)"),
    (45, "Vine", 149.850, "Discovers hidden secrets, builds towers, collapses stone walls", "Civil Infrastructure Demolition & Underground Surveying", "The Urban Subway Tunneling and Infrastructure Boring Era (1960-1995 AD)"),
    (46, "Bifrons", 153.180, "Teaches astrology, geometry, herbs, and moves dead bodies", "Surveying Geometry & Hazardous Waste Management", "The Environmental Protection Agency Hazardous Waste Regulation Era (1970-1990 AD)"),
    (47, "Uvall", 156.510, "Procures love of friends, reconciles enemies, speaks ancient tongues", "Cross-Cultural Mediation & Archaeology Restoration", "The Post-Apartheid Truth and Reconciliation Commission Era (1995-2000 AD)"),
    (48, "Haagenti", 159.840, "Makes men wise, transmutes metals into gold, turns water to wine", "Chemical Engineering & Industrial Transmutation", "The Synthetic Fuel Petrochemical Transformation Era (1970-2000 AD)"),
    (49, "Crocell", 163.170, "Teaches geometry, warms bodies of water, creates roaring sounds", "Geothermal Hydro-Engineering & Computational Geometry", "The Pumped Storage Hydroelectric Infrastructure Era (1970-1990 AD)"),
    (50, "Furcas", 166.500, "Teaches philosophy, astrology, rhetoric, logic, and chiromancy", "Formal Logic Systems & Applied Philosophy", "The Mathematical Logic and Early Computing Formalization Era (1930-1960 AD)"),
    (51, "Balam", 169.830, "Grants perfect memory, foretells past/future, grants invisibility", "High-Density Data Memory Storage & Predictive Modeling", "The Mainframe Database and Relational Data Modeling Era (1970-1995 AD)"),
    (52, "Alloces", 173.160, "Teaches astronomy, liberal arts, provides excellent familiars", "Autonomous Robotics Engineering & Observational Astronomy", "The Hubble Space Telescope and Automated Telemetry Era (1990-2010 AD)"),
    (53, "Camio", 176.490, "Understands bird calls, water sounds, and translates news", "Bio-Acoustic Signal Processing & News Synthesis", "The Global Satellite Broadcasting and News Wire Era (1975-2005 AD)"),
    (54, "Murmur", 179.820, "Teaches philosophy, compels deceased souls to answer questions", "Historical Forensics & Philosophical Logic Inquiry", "The Digital Forensics and Institutional Inquest Era (1980-2010 AD)"),
    (55, "Orobas", 183.150, "Discovers divinity, prevents deception, bestows prelacies/dignities", "Anti-Fraud Compliance & Integrity Verification", "The Basel Banking Accord and Financial Compliance Era (1988-2010 AD)"),
    (56, "Gremory", 186.480, "Reveals hidden treasures, bestows love, foretells future events", "Sub-Surface Geophysical Exploration & Financial Opportunity Forecasting", "The 3D Seismic Geophysical Imaging and Prospecting Era (1980-2010 AD)"),
    (57, "Ose", 189.810, "Teaches secret/divine sciences, changes human shape at will", "Advanced Materials Metamorphism & Molecular Biology", "The Recombinant DNA and Molecular Biotechnology Era (1973-2005 AD)"),
    (58, "Amy", 193.140, "Teaches astrology, liberal arts, reveals hidden treasures", "Astronomical Data Science & Mineral Asset Valuation", "The Digital Geological Information System Era (1990-2015 AD)"),
    (59, "Orias", 196.470, "Teaches virtues of stars, bestows dignities, converts enemies", "Satellite Telecommunications & Executive Reconciliations", "The Global Positioning System (GPS) and Sat-Com Era (1990-2015 AD)"),
    (60, "Vapula", 199.800, "Teaches manual crafts, philosophy, and advanced technical knowledge", "Precision Machining & Advanced Vocational Technical Education", "The Computer-Aided Manufacturing (CAM) Precision Era (1980-2010 AD)"),
    (61, "Zagan", 203.130, "Makes fools wise, turns wine to water, turns metals into gold", "Cognitive Enhancement Systems & Process Optimization", "The Enterprise Resource Planning (ERP) Process Optimization Era (1990-2015 AD)"),
    (62, "Volac", 206.460, "Reveals location of serpents, reveals hidden gold/treasures", "Hazardous Biological Mapping & Precious Metal Geological Survey", "The GIS Environmental Hazard and Mineral Mapping Era (1995-2020 AD)"),
    (63, "Andras", 209.790, "Sows discord, destroys opponents, commands escalation", "Information Warfare & Escalation Dominance Management", "The Cyber Warfare and Information Dominance Era (2000-2025 AD)"),
    (64, "Haures", 213.120, "Destroys enemies by fire, foretells past/future, shields from fraud", "High-Temperature Thermodynamics & Fraud Prevention Systems", "The AI Fraud Detection and Thermal Grid Protection Era (2010-2026 AD)"),
    (65, "Andrealphus", 216.450, "Teaches geometry, measurement, transforms men into birds", "Aerodynamic Geometry & Precision Dimensional Metrology", "The Computational Fluid Dynamics and Aero-Design Era (1990-2020 AD)"),
    (66, "Cimejes", 219.780, "Locates lost treasures, teaches grammar, logic, rhetoric", "Natural Language Processing (NLP) & Resource Asset Discovery", "The Deep Learning and Large Language Model NLP Era (2015-2026 AD)"),
    (67, "Amdusias", 223.110, "Commands trees to bend, provides musical instruments/orchestrations", "Forestry Engineering & Computational Acoustic Design", "The Computational Environmental Acoustics Era (2000-2025 AD)"),
    (68, "Belial", 226.440, "Distributes high titles, reconciles political power, bestows favor", "Political Cabinet Diplomacy & Public Executive Relations", "The Modern Coalition Governance and Executive Diplomacy Era (2000-2026 AD)"),
    (69, "Decarabia", 229.770, "Teaches virtues of birds/herbs, commands illusionary phantoms", "Agricultural Botany & Optical Holography Engineering", "The Precision AgTech and Holographic Simulation Era (2010-2026 AD)"),
    (70, "Seere", 233.100, "Brings instant abundance, teleports items, completes tasks immediately", "Ultra-Low Latency Freight Delivery & Instant Asset Clearing", "The High-Frequency Trading and Instant Logistics Era (2010-2026 AD)"),
    (71, "Dantalion", 236.430, "Reads and alters thoughts of minds, teaches all arts/sciences", "Neural Engineering & Cognitive Interface Analytics", "The Neuro-Tech and Cognitive AI Interface Era (2015-2026 AD)"),
    (72, "Andromalius", 239.760, "Catches thieves, returns stolen goods, reveals hidden conspiracies", "Loss Prevention Operations & Counter-Intelligence Forensics", "The Blockchain Forensics and Automated Compliance Audit Era (2012-2026 AD)")
]

# =====================================================================
# 2. THE 72 ANGELIC PROTOCOLS (SHEM HAMEPHORASH SPECTRUM)
# =====================================================================
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

SCRIPTURE_ANCHOR_REPOSITORY = [
    ("Proverbs 11:3", "The integrity of the upright guides them, but the crookedness of the treacherous destroys them."),
    ("Proverbs 24:3-4", "Through wisdom a house is built, and by understanding it is established; by knowledge the rooms are filled with all precious and pleasant riches."),
    ("Isaiah 2:4", "They shall beat their swords into plowshares, and their spears into pruning hooks; nation shall not lift up sword against nation, neither shall they learn war anymore."),
    ("Isaiah 58:12", "And they that shall be of thee shall build the old waste places: thou shalt raise up the foundations of many generations; and thou shalt be called, The repairer of the breach, The restorer of paths to dwell in."),
    ("Jeremiah 29:11", "For I know the plans I have for you, declares the Lord, plans for welfare and not for evil, to give you a future and a hope."),
    ("Psalm 90:17", "Let the favor of the Lord our God be upon us, and establish the work of our hands upon us; yes, establish the work of our hands!"),
    ("Colossians 3:23", "Whatever you do, work heartily, as for the Lord and not for men."),
    ("Romans 12:2", "Do not be conformed to this world, but be transformed by the renewal of your mind, that by testing you may discern what is the will of God."),
    ("Habakkuk 2:2", "And the Lord answered me: 'Write the vision; make it plain on tablets, so he may run who reads it.'"),
    ("Ecclesiastes 3:1", "For everything there is a season, and a time for every matter under heaven."),
    ("Psalm 119:105", "Your word is a lamp to my feet and a light to my path."),
    ("Job 12:13", "With God are wisdom and might; he has counsel and understanding.")
]

# =====================================================================
# 3. 2000-YEAR CHRONOS DEEP SWEEP (528 AD - 2026 AD) & METRICS CORE
# =====================================================================
def execute_chronos_timeline_sweep(node_name, bottlenecks_count, protocols_count):
    b = max(1, bottlenecks_count)
    p = max(1, protocols_count)
    stoichiometric_ratio = round(b / p, 4)

    node_hash = int(hashlib.sha256(node_name.encode('utf-8')).hexdigest(), 16)
    
    # 2000-Year Chronos Deep Sweep filtering from 528 AD to 2026 AD
    mapped_bottlenecks = []
    total_demonic_freq = 0.0
    for i in range(b):
        # Deterministic 2000-year index mapping across the 72 Goetia vectors
        d_idx = (node_hash + (i * 11)) % 72
        d = DEMONIC_VECTORS[d_idx]
        total_demonic_freq += d[2]
        mapped_bottlenecks.append({
            "vector_id": d[0],
            "name": d[1],
            "frequency": d[2],
            "power": d[3],
            "domain": d[4],
            "historical_era": d[5],
            "string": f"Friction Vector #{d[0]} {d[1]} ({d[3]}): {d[4]}"
        })

    mapped_protocols = []
    total_angelic_freq = 0.0
    for i in range(p):
        a_idx = (node_hash + (i * 17)) % 72
        a = ANGELIC_PROTOCOLS[a_idx]
        total_angelic_freq += a[3]
        mapped_protocols.append({
            "protocol_id": a[0],
            "name": a[1],
            "chorus": a[2],
            "frequency": a[3],
            "power": a[4],
            "domain": a[5],
            "string": f"Angelic Protocol #{a[0]} {a[1]} ({a[2]}): {a[5]}"
        })

    # Node Entropy Index (S_node)
    s_node = 1.05 + ((node_hash % 1400) / 1000.0)

    # 1. UNIFIED GRAND PROPHETIC EQUATION (TTI Calculation)
    avg_demonic_factor = (total_demonic_freq / b) / 100.0
    tti_decay = (stoichiometric_ratio * s_node * (1.85 + avg_demonic_factor)) * 3.14159
    calculated_tti = round(max(15.00, min(99.95, 100.0 - tti_decay)), 2)

    # 2. LAW OF DIMENSIONAL OVERWRITE EQUATION (SHI Calculation)
    avg_angelic_factor = (total_angelic_freq / p) / 600.0
    shi_overwrite_gain = (1.0 - (stoichiometric_ratio * 0.12)) * (0.95 + avg_angelic_factor)
    calculated_shi = round(max(20.00, min(99.99, 90.0 + (shi_overwrite_gain * 9.99))), 2)

    # 3. DIFFERENTIAL DELTA
    calculated_delta = round(abs(calculated_tti - calculated_shi), 2)

    return {
        "bottlenecks_found": b,
        "protocols_applied": p,
        "stoichiometric_ratio": stoichiometric_ratio,
        "node_entropy_index": round(s_node, 3),
        "mapped_bottlenecks": [mb["string"] for mb in mapped_bottlenecks],
        "mapped_bottlenecks_obj": mapped_bottlenecks,
        "mapped_protocols": [mp["string"] for mp in mapped_protocols],
        "mapped_protocols_obj": mapped_protocols,
        "modern_uesp": {
            "tti": calculated_tti,
            "shi": calculated_shi,
            "delta": calculated_delta
        }
    }

def select_dynamic_prophetic_anchor(node_name, tti, shi, delta):
    seed = f"{node_name}_{tti}_{shi}_{delta}"
    hash_val = int(hashlib.sha256(seed.encode('utf-8')).hexdigest(), 16)
    idx = hash_val % len(SCRIPTURE_ANCHOR_REPOSITORY)
    ref, txt = SCRIPTURE_ANCHOR_REPOSITORY[idx]
    
    return {
        "reference": ref,
        "text": txt,
        "source_endpoint": "dynamic_scripture_matrix",
        "context": f"Calculated differential anchor ({delta}) for node {node_name} under technical integrity ({tti}) and systemic health ({shi})."
    }

def synthesize_hybrid_payload(raw_data, calculated_metrics):
    modern = calculated_metrics["modern_uesp"]
    node_name = raw_data.get("node", "Target System Node")

    bottlenecks_obj = calculated_metrics.get("mapped_bottlenecks_obj", [])
    primary_vector = bottlenecks_obj[0] if bottlenecks_obj else {
        "vector_id": 1, "name": "Bael", "power": "Leadership manipulation",
        "domain": "Executive Leadership & Strategic Governance Corruption",
        "historical_era": "The Justinianic Court Intrigues and Imperial Bureaucracy (528-565 AD)"
    }

    protocols_obj = calculated_metrics.get("mapped_protocols_obj", [])
    primary_protocol = protocols_obj[0] if protocols_obj else {
        "protocol_id": 1, "name": "Vehuiah", "chorus": "Seraphim",
        "domain": "Executive Willpower & Innovation Initiation Leadership"
    }

    hist_parallel = raw_data.get("historical_parallel", primary_vector["historical_era"])
    hist_parallel = re.sub(r"^(Parallel Era:\s*)+", "", hist_parallel, flags=re.IGNORECASE)

    analysis_obj = raw_data.get("legacy_vs_modern_analysis", {})
    old_desc = analysis_obj.get("old_way_description", 
        f"During {primary_vector['historical_era']}, civilizations faced friction in {primary_vector['domain']} ({primary_vector['name']}). Lacking real-time automated telemetry, their period approach relied on manual intervention, reactive institutional decrees, and brute-force labor, which ultimately resulted in systemic bottleneck saturation."
    )
    modern_desc = analysis_obj.get("uesp_prce_modern_way", 
        f"To resolve the friction of {primary_vector['name']} ({primary_vector['domain']}) for '{node_name}' today, the UESP framework executes a 2000-year Chronos sweep matching, real-time AI predictive telemetry, stoichiometric friction balancing, and a complete structural dimensional overwrite utilizing {primary_protocol['string']}."
    )
    
    old_desc = re.sub(r'\b(thermodynamic|entropy|energy bandgap|eV|Brus|phonon|quantum)\b', 'structural', old_desc, flags=re.IGNORECASE)
    modern_desc = re.sub(r'\b(thermodynamic|entropy|energy bandgap|eV|Brus|phonon|quantum)\b', 'systemic', modern_desc, flags=re.IGNORECASE)

    anchor_verse_data = select_dynamic_prophetic_anchor(node_name, modern["tti"], modern["shi"], modern["delta"])

    raw_protocol = raw_data.get("protocol", "")
    if len(raw_protocol.split()) < 100:
        raw_protocol = (
            f"Execution Protocol Overview: The system node '{node_name}' under the active influence of Friction Vector #{primary_vector['vector_id']} {primary_vector['name']} "
            f"({primary_vector['power']}) in {primary_vector['domain']} requires an immediate, comprehensive structural overhaul across its operational lifecycle. "
            f"By deploying active UESP protocols rooted in the 2000-year Chronos timeline sweep matching {primary_vector['historical_era']}, we systematically isolate and neutralize "
            "institutional friction vectors and systemic bottlenecks. This intervention bridges historical precedents with advanced predictive analytics, ensuring long-term institutional stability and resilience.\n\n"
            f"Operational Mechanics & Alignment: Every operational layer within the enterprise architecture is cross-referenced against absolute mathematical alignments "
            f"via {primary_protocol['string']}. Rather than relying on trial-and-error reactive measures, the framework executes a precise dimensional overwrite. "
            "Active angelic protocols restore harmony, streamline resource allocation, and fortify governance structures against recurring cycles of entropy and operational decay.\n\n"
            "Future-Proofing & Execution Mandate: Sustained high technical integrity (TTI) and systemic health (SHI) require continuous telemetry monitoring and "
            "automated protocol enforcement. By adhering strictly to calculated stoichiometric ratios and prophetic anchors, the organization secures absolute "
            "operational sovereignty and enduring systemic triumph."
        )

    return {
        "node": node_name,
        "tti": modern["tti"],
        "shi": modern["shi"],
        "delta": modern["delta"],
        "historical_parallel": f"{primary_vector['historical_era']} governed by Friction Vector #{primary_vector['vector_id']} {primary_vector['name']} ({primary_vector['power']})",
        "era_resolution": old_desc,
        "modern_resolution": modern_desc,
        "biblical_tie": {
            "verse": anchor_verse_data["reference"],
            "scripture_text": anchor_verse_data["text"],
            "cdn_endpoint": anchor_verse_data["source_endpoint"],
            "context": anchor_verse_data["context"]
        },
        "protocol": raw_protocol,
        "uesp_final_protocol": raw_protocol,
        "sweep_summary": {
            "bottlenecks_list": calculated_metrics['mapped_bottlenecks'],
            "protocols_list": calculated_metrics['mapped_protocols']
        },
        "legacy_vs_modern_analysis": {
            "old_way_description": old_desc,
            "uesp_prce_modern_way": modern_desc
        },
        "metrics": calculated_metrics,
        "calculated_metrics": calculated_metrics,
        "session_id": raw_data.get("session_id", "")
    }

def clean_and_parse_json(raw_text):
    if not raw_text:
        raise ValueError("Empty response text from LLM.")
    
    text = re.sub(r"<think>.*?</think>", "", raw_text.strip(), flags=re.DOTALL)
    
    code_block_match = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", text, re.DOTALL)
    if code_block_match:
        json_str = code_block_match.group(1)
    else:
        bracket_match = re.search(r"\{.*\}", text, re.DOTALL)
        if not bracket_match:
            raise ValueError("No valid JSON structure found in LLM response.")
        json_str = bracket_match.group(0)

    try:
        return json.loads(json_str)
    except json.JSONDecodeError:
        cleaned = re.sub(r',\s*([\]}])', r'\1', json_str)
        return json.loads(cleaned)

def call_nvidia_endpoint(model_name, prompt, api_key, calculated_metrics):
    client = OpenAI(
        base_url="https://integrate.api.nvidia.com/v1",
        api_key=api_key,
        timeout=120.0
    )

    print(f"[DISPATCH] Executing Ephemeral RAG Instance via model: {model_name}")
    
    completion = client.chat.completions.create(
        model=model_name,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are the UESP PRCE Engine. Provide precise comparative resolutions mapped directly to the 2000-year Chronos sweep (528 AD - 2026 AD). "
                    "For 'old_way_description', detail how the specific historical era from the 2000-year sweep managed or failed to resolve the assigned bottleneck. "
                    "For 'uesp_prce_modern_way', detail the exact real-time UESP stoichiometric overwrite and angelic protocol required today. "
                    "Output strictly valid JSON."
                )
            },
            {"role": "user", "content": prompt}
        ],
        temperature=0.3,
        max_tokens=3000
    )

    content = completion.choices[0].message.content or ""
    try:
        raw_data = clean_and_parse_json(content)
    except Exception:
        raw_data = {}

    final_payload = synthesize_hybrid_payload(raw_data, calculated_metrics)
    return model_name, final_payload

def execute_scan():
    api_key = os.environ.get("NVIDIA_API_KEY")
    if not api_key:
        raise ValueError("[FATAL] NVIDIA_API_KEY environment variable is missing.")

    node = os.getenv("TARGET_NODE", "South Africa Energy Grid")
    session_id = os.getenv("SESSION_ID", "manual_test")

    bottlenecks_count = int(os.getenv("BOTTLENECK_COUNT", "7"))
    protocols_count = int(os.getenv("PROTOCOL_COUNT", "12"))

    calculated_metrics = execute_chronos_timeline_sweep(node, bottlenecks_count, protocols_count)
    primary_vector = calculated_metrics['mapped_bottlenecks_obj'][0]
    primary_protocol = calculated_metrics['mapped_protocols_obj'][0]
    
    prompt = f"""
    Perform an exhaustive 2000-year Chronos Deep Sweep (528 AD - 2026 AD) diagnostic for TARGET NODE: {node}.
    
    CALCULATED CHRONOS SPECTRUM & TIMELINE MAPPINGS:
    - Target Node: {node}
    - 2000-Year Sweep Historical Resonance: {primary_vector['historical_era']}
    - Primary Demonic Friction Vector: {primary_vector['string']}
    - Primary Angelic Protocol: {primary_protocol['string']}
    - Stoichiometric Friction Ratio: {calculated_metrics['stoichiometric_ratio']}
    - Calculated TTI (Unified Grand Prophetic Equation): {calculated_metrics['modern_uesp']['tti']}
    - Calculated SHI (Law of Dimensional Overwrite): {calculated_metrics['modern_uesp']['shi']}
    - Calculated Delta: {calculated_metrics['modern_uesp']['delta']}

    STRICT INSTRUCTIONS:
    1. 'historical_parallel': Output '{primary_vector['historical_era']} governed by {primary_vector['string']}'.
    2. 'old_way_description': Detail specifically how the historical era in {primary_vector['historical_era']} attempted to address {primary_vector['domain']} using period methods.
    3. 'uesp_prce_modern_way': Detail specifically what real-time UESP resolution is applied today to {node} for {primary_vector['domain']} using active mathematical overwrites, stoichiometric balancing, and {primary_protocol['string']}.
    4. 'protocol': Provide an extensive, deep, multi-paragraph executive protocol outlining operational mechanics, systemic forensics, and execution mandates.

    DO NOT USE THERMODYNAMICS, QUANTUM MECHANICS, OR PHYSICS EQUATIONS IN THE TEXT.

    OUTPUT STRICTLY IN THIS JSON FORMAT:
    {{
      "node": "{node}",
      "historical_parallel": "{primary_vector['historical_era']} governed by {primary_vector['string']}",
      "sweep_summary": {{
        "bottlenecks_list": {json.dumps(calculated_metrics['mapped_bottlenecks'])},
        "protocols_list": {json.dumps(calculated_metrics['mapped_protocols'])}
      }},
      "legacy_vs_modern_analysis": {{
        "old_way_description": "During {primary_vector['historical_era']}, civilizations attempted to address {primary_vector['name']} through...",
        "uesp_prce_modern_way": "Today, UESP resolves {primary_vector['name']} in real time for {node} through predictive AI telemetry, stoichiometric balancing, and {primary_protocol['name']}..."
      }},
      "protocol": "Extensive multi-paragraph executive protocol detailing operational alignment, structural forensics, and execution steps...",
      "session_id": "{session_id}"
    }}
    """

    nvidia_models = [
        "meta/llama-3.3-70b-instruct",
        "meta/llama-3.1-70b-instruct",
        "deepseek-ai/deepseek-r1-distill-llama-8b"
    ]

    raw_output = None
    winning_model = None

    print(f"[PARALLEL START] Racing {len(nvidia_models)} Ephemeral RAG Instances across 2000-year Chronos sweep...")
    with ThreadPoolExecutor(max_workers=len(nvidia_models)) as executor:
        futures = {
            executor.submit(
                call_nvidia_endpoint, model, prompt, api_key, calculated_metrics
            ): model for model in nvidia_models
        }

        for future in as_completed(futures):
            model_name = futures[future]
            try:
                winning_model, raw_output = future.result()
                if raw_output:
                    print(f"[VICTORY] Generated unified payload via instance: {winning_model}")
                    break
            except Exception as err:
                print(f"[WARN] Instance ({model_name}) encountered issue: {err}")

    if not raw_output:
        winning_model = "fallback-core"
        raw_output = synthesize_hybrid_payload({
            "node": node,
            "session_id": session_id,
        }, calculated_metrics)

    raw_output['timestamp'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    os.makedirs('data', exist_ok=True)
    with open(f"data/session_{session_id}.json", "w") as f:
        json.dump(raw_output, f, indent=2)
    with open("data/resonance_output.json", "w") as f:
        json.dump(raw_output, f, indent=2)

    print(f"[SUCCESS] 2000-Year Chronos Scan complete for '{node}'. Written to data/resonance_output.json")

if __name__ == "__main__":
    execute_scan()
