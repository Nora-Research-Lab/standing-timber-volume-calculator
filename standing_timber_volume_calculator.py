import math
import matplotlib.pyplot as plt
import io
import base64

# Species default form factors and average reference volumes (m³ for a typical tree)
SPECIES_DEFAULTS = {
    "Douglas-fir": {"form_factor": 0.45, "avg_volume": 0.8},
    "Loblolly Pine": {"form_factor": 0.42, "avg_volume": 0.5},
    "Sugar Maple": {"form_factor": 0.48, "avg_volume": 0.6},
    "Red Oak": {"form_factor": 0.43, "avg_volume": 0.7},
    "generic hardwood": {"form_factor": 0.47, "avg_volume": 0.55},
    "generic softwood": {"form_factor": 0.44, "avg_volume": 0.45}
}

def get_form_factor(species: str, custom_override: float = None) -> float:
    """Return form factor for given species, using custom override if provided."""
    if species not in SPECIES_DEFAULTS:
        raise ValueError(f"Unknown species: {species}")
    if custom_override is not None:
        if custom_override < 0.3 or custom_override > 0.7:
            raise ValueError("Form factor must be between 0.3 and 0.7")
        return custom_override
    return SPECIES_DEFAULTS[species]["form_factor"]

def calculate_individual_volume(dbh_cm: float, height_m: float, form_factor: float) -> float:
    """Calculate individual tree volume in m³ using Smalian's formula (π/4 * D² * H * FF)."""
    if dbh_cm <= 0 or height_m <= 0:
        return 0.0
    dbh_m = dbh_cm / 100.0
    return (math.pi / 4.0) * (dbh_m ** 2) * height_m * form_factor

def calculate_stand_volume(individual_volume_m3: float, trees_per_ha: int) -> float:
    """Calculate volume per hectare."""
    return individual_volume_m3 * trees_per_ha

def convert_to_board_feet(volume_m3: float) -> float:
    """Convert cubic meters to board feet using 1 m³ ≈ 424 bf."""
    return volume_m3 * 424.0

def classify_volume(volume_m3: float) -> str:
    """Classify tree volume into sapling, small, medium, large."""
    if volume_m3 < 0.1:
        return "sapling"
    elif volume_m3 < 0.5:
        return "small"
    elif volume_m3 < 1.0:
        return "medium"
    else:
        return "large"

def get_species_average_volume(species: str) -> float:
    """Return the stored average volume for the species (reference)."""
    if species not in SPECIES_DEFAULTS:
        return 0.0
    return SPECIES_DEFAULTS[species]["avg_volume"]

def generate_comparison_plot(individual_volume_m3: float, species: str):
    """Generate a horizontal bar chart comparing computed volume to species average."""
    species_avg = get_species_average_volume(species)
    categories = ["Computed Volume", "Species Average (Reference)"]
    values = [individual_volume_m3, species_avg]

    fig, ax = plt.subplots(figsize=(6, 3))
    bars = ax.barh(categories, values, color=["#4C72B0", "#55A868"])
    ax.set_xlabel("Volume (m³)")
    ax.set_title(f"Volume Comparison: {species}")

    # Annotate bars with values
    for bar, val in zip(bars, values):
        ax.text(bar.get_width() + 0.01, bar.get_y() + bar.get_height()/2,
                f"{val:.3f}", va='center')

    plt.tight_layout()
    return fig

# # For testing (uncomment to run)
# if __name__ == "__main__":
#     ff = get_form_factor("Douglas-fir")
#     vol = calculate_individual_volume(30, 20, ff)
#     print(vol)
#     fig = generate_comparison_plot(vol, "Douglas-fir")
#     plt.show()
