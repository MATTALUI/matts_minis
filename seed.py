from models import (
    session,
    Mini,
    Color,
    ColorTypes
)
colors = [
    {"type": ColorTypes.primer, "name": "Flat Black", "hex": "#000000", "brand": "Behr"},
    {"type": ColorTypes.primer, "name": "Flat White", "hex": "#ffffff", "brand": "Behr"},

    {"type": ColorTypes.base, "name": "Corak White", "hex": "#ffffff", "brand": "Citadel"},
    {"type": ColorTypes.base, "name": "Abaddon Black", "hex": "#000000", "brand": "Citadel"},
    {"type": ColorTypes.base, "name": "Balthasar Gold", "hex": "#a47552", "brand": "Citadel"},
    {"type": ColorTypes.base, "name": "Macragge Blue", "hex": "#0d407f", "brand": "Citadel"},
    {"type": ColorTypes.wash, "name": "Agrax Earthshade", "hex": "#5a573f", "brand": "Citadel"},
    {"type": ColorTypes.technical, "name": "Astrogranite", "hex": "#757679", "brand": "Citadel"},
    {"type": ColorTypes.base, "name": "Zandri Dust", "hex": "#9e915c", "brand": "Citadel"},
    {"type": ColorTypes.wash, "name": "Coelia Greenshade", "hex": "#0e7f78", "brand": "Citadel"},
    {"type": ColorTypes.base, "name": "Screamer Pink", "hex": "#7c1645", "brand": "Citadel"},
    {"type": ColorTypes.contrast, "name": "Blood Angels Red", "hex": "#9a1115", "brand": "Citadel"},
    {"type": ColorTypes.wash, "name": "Druchii Violet", "hex": "#7a468c", "brand": "Citadel"},
    {"type": ColorTypes.base, "name": "Celedor Sky", "hex": "#396e9e", "brand": "Citadel"},
    {"type": ColorTypes.base, "name": "Naggaroth Night", "hex": "#3d3354", "brand": "Citadel"},
    {"type": ColorTypes.base, "name": "Celestra", "hex": "#90a8a8", "brand": "Citadel"},
    {"type": ColorTypes.wash, "name": "Drakenhof Nightshade", "hex": "#125899", "brand": "Citadel"},
    {"type": ColorTypes.wash, "name": "Seraphim Sepia", "hex": "#d7824b", "brand": "Citadel"},

    {"type": ColorTypes.base, "name": "Bone White", "hex": "#b4bcbb", "brand": "Vallejo"},
    {"type": ColorTypes.base, "name": "Pale Yellow", "hex": "#f8db5d", "brand": "Vallejo"},
    {"type": ColorTypes.base, "name": "Cadmium Skin", "hex": "#f8b185", "brand": "Vallejo"},
    {"type": ColorTypes.base, "name": "Dwarf Skin", "hex": "#f78c5a", "brand": "Vallejo"},
    {"type": ColorTypes.wash, "name": "Flesh Wash", "hex": "#b67c78", "brand": "Vallejo"},
    {"type": ColorTypes.base, "name": "Off White", "hex": "#fdf3da", "brand": "Vallejo"},
    {"type": ColorTypes.base, "name": "Heavy Skintone", "hex": "#ad8468", "brand": "Vallejo"},
    {"type": ColorTypes.base, "name": "Heavy Ochre", "hex": "#ae7727", "brand": "Vallejo"},
    {"type": ColorTypes.wash, "name": "Sepia Wash", "hex": "#8b622b", "brand": "Vallejo"},
    {"type": ColorTypes.base, "name": "Heavy Sienna", "hex": "#5e483c", "brand": "Vallejo"},
    {"type": ColorTypes.base, "name": "Filthy Brown", "hex": "#e99300", "brand": "Vallejo"},
    {"type": ColorTypes.base, "name": "Tan", "hex": "#a85949", "brand": "Vallejo"},

    {"type": ColorTypes.base, "name": "Cadmuim Red Light", "hex": "#c9252c", "brand": "M. Graham"},
    {"type": ColorTypes.base, "name": "QuinaCridon Violet", "hex": "#570925", "brand": "M. Graham"},
]
created_colors = 0
for color in colors:
    q = session.query(Color)
    for key in color:
        value = color.get(key)
        q = q.filter(getattr(Color, key) == value)
    db_color = q.first()
    if not db_color:
        new_color = Color(**color)
        session.add(new_color)
        session.commit()
        created_colors += 1
print(f"Created {created_colors} new colors.")
