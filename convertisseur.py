import streamlit as st

class UnitConverter:
    def __init__(self):
        # Définition de toutes les conversions
        self.conversions = {
            # Masse (g, kg, lb, oz)
            'masse': {
                'g': 1,
                'kg': 1000,
                'mg': 0.001,
                'lb': 453.592,
                'oz': 28.3495
            },
            # Volume (L, m3, gal, pint)
            'volume': {
                'L': 1,
                'm3': 1000,
                'mL': 0.001,
                'gal': 3.78541,
                'pint': 0.473176
            },
            # Pression (Pa, bar, atm, psi)
            'pression': {
                'Pa': 1,
                'bar': 100000,
                'atm': 101325,
                'psi': 6894.76,
                'mmHg': 133.322
            },
            # Température (C, F, K) - Conversion spéciale
            'temperature': {
                'C': {'ratio': 1, 'offset': 0},
                'F': {'ratio': 5/9, 'offset': -32},
                'K': {'ratio': 1, 'offset': -273.15}
            },
            # Énergie (J, cal, kWh)
            'energie': {
                'J': 1,
                'kJ': 1000,
                'cal': 4.184,
                'kcal': 4184,
                'kWh': 3600000,
                'BTU': 1055.06
            },
            # Longueur (m, km, in, ft)
            'longueur': {
                'm': 1,
                'km': 1000,
                'cm': 0.01,
                'mm': 0.001,
                'in': 0.0254,
                'ft': 0.3048,
                'mile': 1609.34
            },
            # Masse volumique (kg/m3, g/cm3, lb/ft3)
            'masse_volumique': {
                'kg/m3': 1,
                'g/cm3': 1000,
                'g/L': 1,
                'lb/ft3': 16.0185
            },
            # Puissance (W, kW, hp)
            'puissance': {
                'W': 1,
                'kW': 1000,
                'MW': 1000000,
                'hp': 745.7
            },
            # Surface (m2, km2, ha, acre)
            'surface': {
                'm2': 1,
                'km2': 1000000,
                'ha': 10000,
                'acre': 4046.86,
                'ft2': 0.092903,
                'in2': 0.00064516
            },
            # Chaleur spécifique (J/kg·K, cal/g·K)
            'chaleur_specifique': {
                'J/(kg·K)': 1,
                'kJ/(kg·K)': 1000,
                'cal/(g·K)': 4184,
                'BTU/(lb·°F)': 4186.8
            },
            # Conductivité thermique (W/m·K, W/cm·K)
            'conductivite_thermique': {
                'W/(m·K)': 1,
                'kW/(m·K)': 1000,
                'W/(cm·K)': 100,
                'cal/(s·cm·K)': 418.4,
                'BTU/(h·ft·°F)': 1.7307
            },
            # Viscosité dynamique (Pa·s, cP, lb·s/ft2)
            'viscosite_dynamique': {
                'Pa·s': 1,
                'cP': 0.001,
                'mPa·s': 0.001,
                'P': 0.1,
                'lb/(ft·s)': 1.48816
            },
            # Viscosité cinématique (m2/s, cSt, ft2/s)
            'viscosite_cinematique': {
                'm2/s': 1,
                'cSt': 0.000001,
                'St': 0.0001,
                'ft2/s': 0.092903
            }
        }

    def convert(self, value, from_unit, to_unit, category):
        """Convertit une valeur d'une unité à une autre dans une catégorie donnée"""
        # Vérification des paramètres
        if category not in self.conversions:
            raise ValueError(f"Catégorie inconnue: {category}")
        
        units = self.conversions[category]
        
        if from_unit not in units or to_unit not in units:
            raise ValueError(f"Unité non reconnue pour {category}")
        
        # Conversion spéciale pour la température
        if category == 'temperature':
            # Convertir vers Celsius en premier
            if from_unit != 'C':
                value = (value + units[from_unit]['offset']) * units[from_unit]['ratio']
            # Convertir depuis Celsius vers l'unité cible
            if to_unit != 'C':
                value = (value / units[to_unit]['ratio']) - units[to_unit]['offset']
            return value
        
        # Conversion standard pour les autres catégories
        valeur_en_base = value * units[from_unit]
        return valeur_en_base / units[to_unit]

    def available_categories(self):
        """Retourne la liste des catégories disponibles"""
        return list(self.conversions.keys())
    
    def available_units(self, category):
        """Retourne la liste des unités disponibles pour une catégorie"""
        if category not in self.conversions:
            raise ValueError(f"Catégorie inconnue: {category}")
        return list(self.conversions[category].keys())

# Interface Streamlit
def main():
    st.set_page_config(page_title="Convertisseur", layout="wide")
    st.title("📐 Convertisseur d'Unités")
    
    # Initialisation du convertisseur
    converter = UnitConverter()
    
    # Sélection de la catégorie
    categories = converter.available_categories()
    category_names = {
        'masse': "Masse",
        'volume': "Volume",
        'pression': "Pression",
        'temperature': "Température",
        'energie': "Énergie",
        'longueur': "Longueur",
        'masse_volumique': "Masse volumique",
        'puissance': "Puissance",
        'surface': "Surface/Aire",
        'chaleur_specifique': "Chaleur spécifique",
        'conductivite_thermique': "Conductivité thermique",
        'viscosite_dynamique': "Viscosité dynamique",
        'viscosite_cinematique': "Viscosité cinématique"
    }
    
    # Sidebar pour la sélection de la catégorie
    with st.sidebar:
        st.header("Configuration")
        selected_category = st.selectbox(
            "Sélectionnez une catégorie de conversion",
            options=categories,
            format_func=lambda x: category_names.get(x, x)
        )
        
        # Afficher les unités disponibles pour la catégorie sélectionnée
        st.subheader("Unités disponibles")
        units = converter.available_units(selected_category)
        for unit in units:
            st.write(f"- {unit}")
    
    # Interface principale
    col1, col2, col3 = st.columns(3)
    
    with col1:
        from_unit = st.selectbox(
            "De",
            options=converter.available_units(selected_category),
            key="from_unit"
        )
    
    with col2:
        value = st.number_input(
            "Valeur",
            value=1.0,
            step=0.1,
            key="value"
        )
    
    with col3:
        to_unit = st.selectbox(
            "Vers",
            options=converter.available_units(selected_category),
            key="to_unit"
        )
    
    # Bouton de conversion
    if st.button("Convertir"):
        try:
            result = converter.convert(value, from_unit, to_unit, selected_category)
            # Formatage du résultat avec séparateur de milliers (espace)
            formatted_result = f"{result:,.0f}".replace(",", " ")
            st.success(f"**Résultat :** {value} {from_unit} = {formatted_result} {to_unit}")
        except Exception as e:
            st.error(f"Erreur lors de la conversion: {str(e)}")
    
    # Section d'exemples
    st.markdown("---")
    st.subheader("Exemples rapides")
    
    examples = {
        'masse': ("500 g en kg", 500, 'g', 'kg'),
        'temperature': ("100 °C en °F", 100, 'C', 'F'),
        'pression': ("1 atm en Pa", 1, 'atm', 'Pa'),
        'energie': ("1 kWh en J", 1, 'kWh', 'J'),
        'longueur': ("1 mile en km", 1, 'mile', 'km')
    }
    
    if selected_category in examples:
        desc, val, frm, to = examples[selected_category]
        if st.button(f"Exemple: {desc}"):
            result = converter.convert(val, frm, to, selected_category)
            st.info(f"**{desc}** = {result:.6g} {to}")

if __name__ == "__main__":
    main()