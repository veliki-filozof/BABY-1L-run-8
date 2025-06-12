import openmc
from libra_toolbox.neutronics.neutron_source import A325_generator_diamond
from libra_toolbox.neutronics import vault
import helpers


def baby_geometry(x_c: float, y_c: float, z_c: float):
    """Returns the geometry for the BABY experiment.

    Args:
        x_c: x-coordinate of the center of the BABY experiment (cm)
        y_c: y-coordinate of the center of the BABY experiment (cm)
        z_c: z-coordinate of the center of the BABY experiment (cm)

    Returns:
        the sphere, cllif cell, and cells
    """

    epoxy_thickness = 2.54  # 1 inch
    alumina_compressed_thickness = 2.54  # 1 inch
    base_thickness = 0.786
    alumina_thickness = 0.635
    he_thickness = 0.6
    inconel_thickness = 0.3
    heater_gap = 0.878
    cllif_thickness = 6.388 + 0.13022  # without heater: 0.1081
    gap_thickness = 4.605
    cap = 1.422
    firebrick_thickness = 15.24
    high = 21.093
    cover = 2.392
    z_tab = 28.00
    lead_height = 4.00
    lead_width = 8.00
    lead_length = 16.00
    heater_r = 0.439
    heater_h = 25.40
    heater_z = (
        epoxy_thickness
        + alumina_compressed_thickness
        + base_thickness
        + alumina_thickness
        + he_thickness
        + inconel_thickness
        + heater_gap
        + z_c
    )

    cllif_radius = 7.00
    inconel_radius = 7.3
    he_radius = 9.144
    firebrick_radius = 12.002
    vessel_radius = 12.853
    external_radius = 13.272

    source_h = 50.00
    source_x = x_c - 13.50
    source_z = z_c - 5.635
    source_external_r = 5.00
    source_internal_r = 4.75

    ######## Surfaces #################
    z_plane_1 = openmc.ZPlane(0.0 + z_c)
    z_plane_2 = openmc.ZPlane(epoxy_thickness + z_c)
    z_plane_3 = openmc.ZPlane(epoxy_thickness + alumina_compressed_thickness + z_c)
    z_plane_4 = openmc.ZPlane(
        epoxy_thickness + alumina_compressed_thickness + base_thickness + z_c
    )
    z_plane_5 = openmc.ZPlane(
        epoxy_thickness
        + alumina_compressed_thickness
        + base_thickness
        + alumina_thickness
        + z_c
    )
    z_plane_6 = openmc.ZPlane(
        epoxy_thickness
        + alumina_compressed_thickness
        + base_thickness
        + alumina_thickness
        + he_thickness
        + z_c
    )
    z_plane_7 = openmc.ZPlane(
        epoxy_thickness
        + alumina_compressed_thickness
        + base_thickness
        + alumina_thickness
        + he_thickness
        + inconel_thickness
        + z_c
    )
    z_plane_8 = openmc.ZPlane(
        epoxy_thickness
        + alumina_compressed_thickness
        + base_thickness
        + alumina_thickness
        + he_thickness
        + inconel_thickness
        + cllif_thickness
        + z_c
    )
    z_plane_9 = openmc.ZPlane(
        epoxy_thickness
        + alumina_compressed_thickness
        + base_thickness
        + alumina_thickness
        + he_thickness
        + inconel_thickness
        + cllif_thickness
        + gap_thickness
        + z_c
    )
    z_plane_10 = openmc.ZPlane(
        epoxy_thickness
        + alumina_compressed_thickness
        + base_thickness
        + alumina_thickness
        + he_thickness
        + inconel_thickness
        + cllif_thickness
        + gap_thickness
        + cap
        + z_c
    )
    z_plane_11 = openmc.ZPlane(
        epoxy_thickness
        + alumina_compressed_thickness
        + base_thickness
        + alumina_thickness
        + firebrick_thickness
        + z_c
    )
    z_plane_12 = openmc.ZPlane(
        epoxy_thickness + alumina_compressed_thickness + base_thickness + high + z_c
    )
    z_plane_13 = openmc.ZPlane(
        epoxy_thickness
        + alumina_compressed_thickness
        + base_thickness
        + high
        + cover
        + z_c
    )
    z_plane_14 = openmc.ZPlane(z_c - z_tab)
    z_plane_15 = openmc.ZPlane(z_c - z_tab - epoxy_thickness)

    ######## Cylinder #################
    z_cyl_1 = openmc.ZCylinder(x0=x_c, y0=y_c, r=cllif_radius)
    z_cyl_2 = openmc.ZCylinder(x0=x_c, y0=y_c, r=inconel_radius)
    z_cyl_3 = openmc.ZCylinder(x0=x_c, y0=y_c, r=he_radius)
    z_cyl_4 = openmc.ZCylinder(x0=x_c, y0=y_c, r=firebrick_radius)
    z_cyl_5 = openmc.ZCylinder(x0=x_c, y0=y_c, r=vessel_radius)
    z_cyl_6 = openmc.ZCylinder(x0=x_c, y0=y_c, r=external_radius)

    right_cyl = openmc.model.RightCircularCylinder(
        (x_c, y_c, heater_z), heater_h, heater_r, axis="z"
    )
    ext_cyl_source = openmc.model.RightCircularCylinder(
        (source_x, y_c, source_z), source_h, source_external_r, axis="x"
    )
    source_region = openmc.model.RightCircularCylinder(
        (source_x + 0.25, y_c, source_z), source_h - 0.50, source_internal_r, axis="x"
    )

    ######## Sphere #################
    sphere = openmc.Sphere(x0=x_c, y0=y_c, z0=z_c, r=50.00)  # before r=50.00

    ######## Lead bricks positioned under the source #################
    positions = [
        (x_c - 13.50, y_c, z_c - z_tab),
        (x_c - 4.50, y_c, z_c - z_tab),
        (x_c + 36.50, y_c, z_c - z_tab),
        (x_c + 27.50, y_c, z_c - z_tab),
    ]

    lead_blocks = []
    for position in positions:
        lead_block_region = openmc.model.RectangularParallelepiped(
            position[0] - lead_width / 2,
            position[0] + lead_width / 2,
            position[1] - lead_length / 2,
            position[1] + lead_length / 2,
            position[2],
            position[2] + lead_height,
        )
        lead_blocks.append(lead_block_region)

    # regions
    source_wall_region = -ext_cyl_source & +source_region
    source_region = -source_region
    epoxy_region = +z_plane_1 & -z_plane_2 & -sphere
    alumina_compressed_region = +z_plane_2 & -z_plane_3 & -sphere
    bottom_vessel = +z_plane_3 & -z_plane_4 & -z_cyl_6
    top_vessel = +z_plane_12 & -z_plane_13 & -z_cyl_6 & +right_cyl
    cylinder_vessel = +z_plane_4 & -z_plane_12 & +z_cyl_5 & -z_cyl_6
    vessel_region = bottom_vessel | cylinder_vessel | top_vessel
    alumina_region = +z_plane_4 & -z_plane_5 & -z_cyl_5
    bottom_cap = +z_plane_6 & -z_plane_7 & -z_cyl_2 & +right_cyl
    cylinder_cap = +z_plane_7 & -z_plane_9 & +z_cyl_1 & -z_cyl_2 & +right_cyl
    top_cap = +z_plane_9 & -z_plane_10 & -z_cyl_2 & +right_cyl
    cap_region = bottom_cap | cylinder_cap | top_cap
    cllif_region = +z_plane_7 & -z_plane_8 & -z_cyl_1 & +right_cyl
    gap_region = +z_plane_8 & -z_plane_9 & -z_cyl_1 & +right_cyl
    firebrick_region = +z_plane_5 & -z_plane_11 & +z_cyl_3 & -z_cyl_4
    heater_region = -right_cyl
    table_under_source_region = +z_plane_15 & -z_plane_14 & -sphere
    lead_block_1_region = -lead_blocks[0]
    lead_block_2_region = -lead_blocks[1]
    lead_block_3_region = -lead_blocks[2]
    lead_block_4_region = -lead_blocks[3]
    he_region = (
        +z_plane_5
        & -z_plane_12
        & -z_cyl_5
        & ~source_region
        & ~epoxy_region
        & ~alumina_compressed_region
        & ~alumina_region
        & ~cllif_region
        & ~gap_region
        & ~firebrick_region
        & ~vessel_region
        & ~cap_region
        & ~heater_region
        & ~table_under_source_region
        & ~lead_block_1_region
        & ~lead_block_2_region
        & ~lead_block_3_region
        & ~lead_block_4_region
    )
    sphere_region = (
        -sphere
        & ~source_wall_region
        & ~source_region
        & ~epoxy_region
        & ~alumina_compressed_region
        & ~alumina_region
        & ~cllif_region
        & ~gap_region
        & ~firebrick_region
        & ~he_region
        & ~vessel_region
        & ~cap_region
        & ~heater_region
        & ~table_under_source_region
        & ~lead_block_1_region
        & ~lead_block_2_region
        & ~lead_block_3_region
        & ~lead_block_4_region
    )

    # cells
    source_wall_cell_1 = openmc.Cell(region=source_wall_region)
    source_wall_cell_1.fill = SS304
    source_region = openmc.Cell(region=source_region)
    source_region.fill = None
    epoxy_cell = openmc.Cell(region=epoxy_region)
    epoxy_cell.fill = epoxy
    alumina_compressed_cell = openmc.Cell(region=alumina_compressed_region)
    alumina_compressed_cell.fill = alumina
    vessel_cell = openmc.Cell(region=vessel_region)
    vessel_cell.fill = inconel625
    alumina_cell = openmc.Cell(region=alumina_region)
    alumina_cell.fill = alumina
    cllif_cell = openmc.Cell(region=cllif_region)
    cllif_cell.fill = cllif_nat  # cllif_nat or lithium_lead
    gap_cell = openmc.Cell(region=gap_region)
    gap_cell.fill = he
    cap_cell = openmc.Cell(region=cap_region)
    cap_cell.fill = inconel625
    firebrick_cell = openmc.Cell(region=firebrick_region)
    firebrick_cell.fill = firebrick
    heater_cell = openmc.Cell(region=heater_region)
    heater_cell.fill = heater_mat
    table_cell = openmc.Cell(region=table_under_source_region)
    table_cell.fill = epoxy
    sphere_cell = openmc.Cell(region=sphere_region)
    sphere_cell.fill = air
    he_cell = openmc.Cell(region=he_region)
    he_cell.fill = he
    lead_block_1_cell = openmc.Cell(region=lead_block_1_region)
    lead_block_1_cell.fill = lead
    lead_block_2_cell = openmc.Cell(region=lead_block_2_region)
    lead_block_2_cell.fill = lead
    lead_block_3_cell = openmc.Cell(region=lead_block_3_region)
    lead_block_3_cell.fill = lead
    lead_block_4_cell = openmc.Cell(region=lead_block_4_region)
    lead_block_4_cell.fill = lead

    cells = [
        source_wall_cell_1,
        source_region,
        epoxy_cell,
        alumina_compressed_cell,
        vessel_cell,
        alumina_cell,
        cap_cell,
        cllif_cell,
        gap_cell,
        firebrick_cell,
        heater_cell,
        he_cell,
        sphere_cell,
        table_cell,
        lead_block_1_cell,
        lead_block_2_cell,
        lead_block_3_cell,
        lead_block_4_cell,
    ]

    return sphere, cllif_cell, cells


def baby_model():
    """Returns an openmc model of the BABY experiment.

    Returns:
        the openmc model
    """

    materials = [
        inconel625,
        cllif_nat,
        SS304,
        heater_mat,
        firebrick,
        alumina,
        lead,
        air,
        epoxy,
        he,
    ]

    # BABY coordinates
    x_c = 587  # cm
    y_c = 60  # cm
    z_c = 100  # cm
    sphere, cllif_cell, cells = baby_geometry(x_c, y_c, z_c)

    ############################################################################
    # Define Settings

    settings = openmc.Settings()

    src = A325_generator_diamond((x_c, y_c, z_c - 5.635), (1, 0, 0))
    settings.source = src
    settings.batches = 100
    settings.inactive = 0
    settings.run_mode = "fixed source"
    settings.particles = int(1e4)
    settings.output = {"tallies": False}
    settings.photon_transport = False

    ############################################################################
    overall_exclusion_region = -sphere

    ############################################################################
    # Specify Tallies
    tallies = openmc.Tallies()

    tbr_tally = openmc.Tally(name="TBR")
    tbr_tally.scores = ["(n,Xt)"]
    tbr_tally.filters = [openmc.CellFilter(cllif_cell)]
    tallies.append(tbr_tally)

    model = vault.build_vault_model(
        settings=settings,
        tallies=tallies,
        added_cells=cells,
        added_materials=materials,
        overall_exclusion_region=overall_exclusion_region,
    )

    return model


############################################################################
# Define Materials
# Source: PNNL Materials Compendium April 2021
# PNNL-15870, Rev. 2
inconel625 = openmc.Material(name="Inconel 625")
inconel625.add_element("C", 0.000990, "wo")
inconel625.add_element("Al", 0.003960, "wo")
inconel625.add_element("Si", 0.004950, "wo")
inconel625.add_element("P", 0.000148, "wo")
inconel625.add_element("S", 0.000148, "wo")
inconel625.add_element("Ti", 0.003960, "wo")
inconel625.add_element("Cr", 0.215000, "wo")
inconel625.add_element("Mn", 0.004950, "wo")
inconel625.add_element("Fe", 0.049495, "wo")
inconel625.add_element("Co", 0.009899, "wo")
inconel625.add_element("Ni", 0.580000, "wo")
inconel625.add_element("Nb", 0.036500, "wo")
inconel625.add_element("Mo", 0.090000, "wo")
inconel625.set_density("g/cm3", 8.44)

# lif-licl - natural - pure
licl_frac = 0.695
cllif_nat = openmc.Material(name="ClLiF natural")
cllif_nat.add_element("F", 0.5 * (1 - licl_frac), "ao")
cllif_nat.add_element("Li", 0.5 * (1 - licl_frac) + 0.5 * licl_frac, "ao")
cllif_nat.add_element("Cl", 0.5 * licl_frac, "ao")
cllif_nat.set_density(
    "g/cm3", helpers.get_exp_cllif_density(650)
)  # 69.5 at. % LiCL at 650 C

# Stainless Steel 304 from PNNL Materials Compendium (PNNL-15870 Rev2)
SS304 = openmc.Material(name="Stainless Steel 304")
# SS304.temperature = 700 + 273
SS304.add_element("C", 0.000800, "wo")
SS304.add_element("Mn", 0.020000, "wo")
SS304.add_element("P", 0.000450, "wo")
SS304.add_element("S", 0.000300, "wo")
SS304.add_element("Si", 0.010000, "wo")
SS304.add_element("Cr", 0.190000, "wo")
SS304.add_element("Ni", 0.095000, "wo")
SS304.add_element("Fe", 0.683450, "wo")
SS304.set_density("g/cm3", 8.00)

heater_mat = openmc.Material(name="heater")
heater_mat.add_element("C", 0.000990, "wo")
heater_mat.add_element("Al", 0.003960, "wo")
heater_mat.add_element("Si", 0.004950, "wo")
heater_mat.add_element("P", 0.000148, "wo")
heater_mat.add_element("S", 0.000148, "wo")
heater_mat.add_element("Ti", 0.003960, "wo")
heater_mat.add_element("Cr", 0.215000, "wo")
heater_mat.add_element("Mn", 0.004950, "wo")
heater_mat.add_element("Fe", 0.049495, "wo")
heater_mat.add_element("Co", 0.009899, "wo")
heater_mat.add_element("Ni", 0.580000, "wo")
heater_mat.add_element("Nb", 0.036500, "wo")
heater_mat.add_element("Mo", 0.090000, "wo")
heater_mat.set_density("g/cm3", 2.44)

# Using Microtherm with 1 a% Al2O3, 27 a% ZrO2, and 72 a% SiO2
# https://www.foundryservice.com/product/microporous-silica-insulating-boards-mintherm-microtherm-1925of-grades/
firebrick = openmc.Material(name="Firebrick")
# Estimate average temperature of Firebrick to be around 300 C
# Firebrick.temperature = 273 + 300
firebrick.add_element("Al", 0.004, "ao")
firebrick.add_element("O", 0.666, "ao")
firebrick.add_element("Si", 0.240, "ao")
firebrick.add_element("Zr", 0.090, "ao")
firebrick.set_density("g/cm3", 0.30)

# alumina insulation
# data from https://precision-ceramics.com/materials/alumina/
alumina = openmc.Material(name="Alumina insulation")
alumina.add_element("O", 0.6, "ao")
alumina.add_element("Al", 0.4, "ao")
alumina.set_density("g/cm3", 3.98)

# air
air = openmc.Material(name="Air")
air.add_element("C", 0.00012399, "wo")
air.add_element("N", 0.75527, "wo")
air.add_element("O", 0.23178, "wo")
air.add_element("Ar", 0.012827, "wo")
air.set_density("g/cm3", 0.0012)

# epoxy
epoxy = openmc.Material(name="Epoxy")
epoxy.add_element("C", 0.70, "wo")
epoxy.add_element("H", 0.08, "wo")
epoxy.add_element("O", 0.15, "wo")
epoxy.add_element("N", 0.07, "wo")
epoxy.set_density("g/cm3", 1.2)

# helium @5psig
pressure = 34473.8  # Pa ~ 5 psig
temperature = 300  # K
R_he = 2077  # J/(kg*K)
density = pressure / (R_he * temperature) / 1000  # in g/cm^3
he = openmc.Material(name="Helium")
he.add_element("He", 1.0, "ao")
he.set_density("g/cm3", density)

# lead
# data from https://wwwrcamnl.wr.usgs.gov/isoig/period/pb_iig.html
lead = openmc.Material()
lead.set_density("g/cm3", 11.34)
lead.add_nuclide("Pb204", 0.014, "ao")
lead.add_nuclide("Pb206", 0.241, "ao")
lead.add_nuclide("Pb207", 0.221, "ao")
lead.add_nuclide("Pb208", 0.524, "ao")


if __name__ == "__main__":
    model = baby_model()
    model.run()
    sp = openmc.StatePoint(f"statepoint.{model.settings.batches}.h5")
    tbr_tally = sp.get_tally(name="TBR").get_pandas_dataframe()

    print(f"TBR: {tbr_tally['mean'].iloc[0] :.6e}\n")
    print(f"TBR std. dev.: {tbr_tally['std. dev.'].iloc[0] :.6e}\n")

    processed_data = {
        "modelled_TBR": {
            "mean": tbr_tally["mean"].iloc[0],
            "std_dev": tbr_tally["std. dev."].iloc[0],
        }
    }

    import json

    processed_data_file = "../../data/processed_data.json"

    try:
        with open(processed_data_file, "r") as f:
            existing_data = json.load(f)
    except FileNotFoundError:
        print(f"Processed data file not found, creating it in {processed_data_file}")
        existing_data = {}

    existing_data.update(processed_data)

    with open(processed_data_file, "w") as f:
        json.dump(existing_data, f, indent=4)

    print(f"Processed data stored in {processed_data_file}")
