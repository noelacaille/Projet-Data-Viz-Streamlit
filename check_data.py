"""
Data validation script - Run this before launching the app to check data integrity.

Usage:
    python check_data.py
"""

import sys
from pathlib import Path
import pandas as pd


def check_file_exists(filepath: Path) -> bool:
    """Check if a file exists."""
    if not filepath.exists():
        print(f"❌ ERREUR : Fichier non trouvé : {filepath}")
        return False
    print(f"✅ Fichier trouvé : {filepath.name}")
    return True


def check_csv_structure(filepath: Path, expected_columns: list) -> bool:
    """Check if CSV has expected columns."""
    try:
        df = pd.read_csv(filepath, nrows=5)
        missing = set(expected_columns) - set(df.columns)
        if missing:
            print(f"❌ ERREUR : Colonnes manquantes dans {filepath.name}: {missing}")
            return False
        print(f"✅ Structure valide : {filepath.name} ({len(df.columns)} colonnes)")
        return True
    except Exception as e:
        print(f"❌ ERREUR : Impossible de lire {filepath.name}: {e}")
        return False


def check_data_quality(filepath: Path) -> dict:
    """Check data quality metrics."""
    try:
        df = pd.read_csv(filepath)
        metrics = {
            'rows': len(df),
            'columns': len(df.columns),
            'missing': df.isnull().sum().sum(),
            'duplicates': df.duplicated().sum()
        }
        return metrics
    except Exception as e:
        print(f"❌ ERREUR : Impossible d'analyser {filepath.name}: {e}")
        return None


def main():
    """Main validation function."""
    print("="*60)
    print("🔍 VÉRIFICATION DES DONNÉES - Dashboard Mobilité")
    print("="*60)
    print()
    
    # Define paths
    base_dir = Path(__file__).parent
    data_dir = base_dir / "data"
    
    commute_file = data_dir / "flux-domicile-travail-selon-le-mode-de-transport-principal-utilise-commune.csv"
    geo_file = data_dir / "20230823-communes-departement-region.csv"
    
    all_ok = True
    
    # Check 1: Directory exists
    print("📁 Vérification du dossier data/")
    if not data_dir.exists():
        print(f"❌ ERREUR : Le dossier {data_dir} n'existe pas !")
        print("   Créez-le et placez-y les fichiers CSV.")
        return False
    print("✅ Dossier data/ trouvé")
    print()
    
    # Check 2: Files exist
    print("📄 Vérification des fichiers...")
    all_ok &= check_file_exists(commute_file)
    all_ok &= check_file_exists(geo_file)
    print()
    
    if not all_ok:
        print("❌ Des fichiers sont manquants. Téléchargez-les depuis les sources indiquées dans le README.")
        return False
    
    # Check 3: CSV structure
    print("🔍 Vérification de la structure...")
    commute_columns = ['date_mesure', 'geocode_commune', 'libelle_commune', 'mode_transport', 'valeur']
    geo_columns = ['code_commune_INSEE', 'nom_commune', 'latitude', 'longitude', 
                   'code_departement', 'nom_departement', 'code_region', 'nom_region']
    
    all_ok &= check_csv_structure(commute_file, commute_columns)
    all_ok &= check_csv_structure(geo_file, geo_columns)
    print()
    
    if not all_ok:
        print("❌ La structure des fichiers n'est pas conforme.")
        return False
    
    # Check 4: Data quality
    print("📊 Analyse de la qualité des données...")
    
    print("\n🚗 Fichier des flux domicile-travail :")
    commute_metrics = check_data_quality(commute_file)
    if commute_metrics:
        print(f"   • Lignes : {commute_metrics['rows']:,}".replace(',', ' '))
        print(f"   • Colonnes : {commute_metrics['columns']}")
        print(f"   • Valeurs manquantes : {commute_metrics['missing']}")
        print(f"   • Doublons : {commute_metrics['duplicates']}")
        
        if commute_metrics['rows'] < 100000:
            print("   ⚠️  ATTENTION : Nombre de lignes anormalement bas")
    
    print("\n🗺️ Fichier géographique :")
    geo_metrics = check_data_quality(geo_file)
    if geo_metrics:
        print(f"   • Lignes : {geo_metrics['rows']:,}".replace(',', ' '))
        print(f"   • Colonnes : {geo_metrics['columns']}")
        print(f"   • Valeurs manquantes : {geo_metrics['missing']}")
        print(f"   • Doublons : {geo_metrics['duplicates']}")
        
        if geo_metrics['rows'] < 30000:
            print("   ⚠️  ATTENTION : Nombre de communes anormalement bas")
    
    print()
    
    # Check 5: Merge test
    print("🔗 Test de fusion des données...")
    try:
        df_commute = pd.read_csv(commute_file, nrows=1000)
        df_geo = pd.read_csv(geo_file)
        
        merged = df_commute.merge(
            df_geo,
            left_on='geocode_commune',
            right_on='code_commune_INSEE',
            how='left'
        )
        
        match_rate = (merged['nom_commune'].notna().sum() / len(merged)) * 100
        print(f"✅ Taux de correspondance : {match_rate:.1f}%")
        
        if match_rate < 80:
            print("⚠️  ATTENTION : Taux de correspondance faible")
    except Exception as e:
        print(f"❌ ERREUR lors du test de fusion : {e}")
        all_ok = False
    
    print()
    print("="*60)
    
    if all_ok:
        print("✅ VALIDATION RÉUSSIE !")
        print("   Vous pouvez lancer l'application avec : streamlit run app.py")
    else:
        print("❌ VALIDATION ÉCHOUÉE")
        print("   Corrigez les erreurs ci-dessus avant de lancer l'application.")
    
    print("="*60)
    
    return all_ok


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
