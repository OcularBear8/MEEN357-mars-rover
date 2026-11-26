import matplotlib.pyplot as plt

def analyze_batt(battery_type):

    if battery_type.lower() == 'LiFePO4'.lower():
        mass_per_module = 3.4860        # kg
        Joules_per_module = 0.9072e5   # Joules (7 AHr @ 36 V)
        cost_per_module = 2.25e5          # $ (retail)
    elif battery_type.lower() == 'NiMH'.lower():
        # 3x Tenergy 12V module made from sub-C cell NiMH batteries
        # 5000 mAhr per module
        mass_per_module = 2.1630        # kg
        Joules_per_module = 0.6480e5    # Joules (5000 mAhr @ 36V)
        cost_per_module = 125000        # $ (retail reflecting quantity discount)
    elif battery_type.lower() == 'NiCD'.lower():
        # 3x 12V module made from AA cell NiCD batteries
        # 700 mAHr capacity per module
        mass_per_module = 0.669        # kg
        Joules_per_module = 0.0906e5   # Joules (700 mAhr @ 36V)
        cost_per_module = 25000           # $ (retail reflecting quantity discount)
    elif battery_type.lower() == 'PbAcid-1'.lower():
        # 3x UPG D5722 Sealed Lead Acid
        mass_per_module = 30        # kg
        Joules_per_module = 4.38e5    # Joules (35 AHr @ 36V)
        cost_per_module = 150000           # $ (full retail)
    elif battery_type.lower() == 'PbAcid-2'.lower():
        # UPG UB-GC2 Golf Cart/AGM Battery - Sealed Lead Acid
        # factored below at x6 since each of the above is only 6V DC
        mass_per_module   = 60         # kg
        Joules_per_module = 8.76e5     # Joules (200 AHr @ 36V)
        cost_per_module   = 21000          # $ (full retail)
    elif battery_type.lower() == 'PbAcid-3'.lower():
        # 3x Powersonic PS-12180NB 12V 18Ah Sealed Lead Acid Battery
        mass_per_module   = 45         # kg
        Joules_per_module = 6.57e5    # Joules (18 AHr @ 36V)
        cost_per_module   = 170000           # $ (full retail)
    else:
        raise Exception('define_batt_pack: unknown battery battery_type')

    joules_per_kg = Joules_per_module / mass_per_module
    cost_per_joule = cost_per_module / Joules_per_module

    return joules_per_kg, cost_per_joule

batteries_types = ['LiFePO4','NiMH','NiCD','PbAcid-1','PbAcid-2','PbAcid-3']

fig, ax = plt.subplots()

X = []
Y = []

for i in batteries_types:

    x, y = analyze_batt(i)

    X.append(x)
    Y.append(y)

    ax.annotate(
        f'{i}',                      # Label text
        (x,y),                     # Point to label
        textcoords="offset points",   # Position relative to the point
        xytext=(0, 8),                # 8 points vertically above the marker
        ha='right'                   # Horizontal alignment
    )

ax.plot(X,Y, 'bo')
ax.set_xlabel('Joules per kg')
ax.set_ylabel('$ per Joule')
plt.show()