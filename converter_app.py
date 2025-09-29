import streamlit as st
import requests

# ------------------ Page Config ------------------
st.set_page_config(page_title="Travelers' Unit Converter", layout="centered")
st.title("🔄 Travelers' Unit Converter")

# ------------------ Helper Dictionaries ------------------
unit_types = {
    "Length": {
        "in": {"cm": 2.54, "m": 0.0254, "ft": 0.0833333},
        "cm": {"in": 0.393701, "m": 0.01, "ft": 0.0328084},
        "m": {"in": 39.3701, "cm": 100, "ft": 3.28084},
        "ft": {"in": 12, "cm": 30.48, "m": 0.3048},
    },
    "Speed": {
        "km/h": {"mph": 0.621371},
        "mph": {"km/h": 1.60934},
    },
    "Volume": {
        "gal": {"L": 3.78541},
        "L": {"gal": 0.264172},
    },
    "Mass": {
        "lb": {"oz": 16, "kg": 0.453592},
        "oz": {"lb": 0.0625, "kg": 0.0283495},
        "kg": {"lb": 2.20462, "oz": 35.274},
    },
}

# ------------------ Sidebar: Converter Selection ------------------
converter_choice = st.sidebar.selectbox(
    "Select Converter Type",
    ["Currency", "Length", "Speed", "Volume", "Mass", "Temperature"]
)

# ------------------ Currency Converter ------------------
if converter_choice == "Currency":
    st.subheader("💰 Currency Converter")
    base = st.text_input("Base Currency (e.g., USD):", "USD").upper()
    target = st.text_input("Target Currency (e.g., EUR):", "EUR").upper()
    amount = st.number_input("Amount:", value=1.0, format="%.4f")

    if st.button("Convert"):
        if amount < 0:
            st.error("❌ Amount cannot be negative!")
        else:
            url = f"https://v6.exchangerate-api.com/v6/42e07609c352e07befd0aa1c/latest/{base}"
            try:
                response = requests.get(url, timeout=5)
                data = response.json()
                if data.get("result") == "success":
                    rate = data["conversion_rates"].get(target)
                    if rate:
                        converted = amount * rate
                        st.success(
                            f"{amount} {base} = {converted:.2f} {target}")
                    else:
                        st.error(f"❌ Unsupported target currency: {target}")
                else:
                    st.error("❌ Failed to fetch exchange rate data!")
            except Exception as e:
                st.error(f"❌ Error fetching data: {e}")

# ------------------ General Unit Converters ------------------
elif converter_choice in ["Length", "Speed", "Volume", "Mass"]:
    st.subheader(f"📏 {converter_choice} Converter")
    units_dict = unit_types[converter_choice]
    value = st.number_input(
        f"Value to convert ({converter_choice}):", value=1.0)
    from_unit = st.selectbox("Original Unit:", list(units_dict.keys()))
    to_unit = st.selectbox("Target Unit:", list(units_dict.keys()), index=1)

    if st.button(f"Convert {converter_choice}"):
        if value < 0:
            st.error("❌ Value cannot be negative for this unit type!")
        elif from_unit == to_unit:
            st.success(f"{value} {from_unit} = {value} {to_unit}")
        else:
            try:
                converted = value * units_dict[from_unit][to_unit]
                st.success(f"{value} {from_unit} = {converted:.4f} {to_unit}")
            except KeyError:
                st.error("❌ Unsupported unit conversion!")

# ------------------ Temperature Converter ------------------
elif converter_choice == "Temperature":
    st.subheader("🌡️ Temperature Converter")
    temp = st.number_input("Temperature Value:", value=25.0)
    from_unit = st.selectbox("Original Unit:", ["C", "F", "K"], index=0)
    to_unit = st.selectbox("Target Unit:", ["C", "F", "K"], index=1)

    if st.button("Convert Temperature"):
        f = from_unit.upper()
        t = to_unit.upper()
        res = None
        if f == "C":
            if t == "F":
                res = temp * 9/5 + 32
            elif t == "K":
                res = temp + 273.15
            else:
                res = temp
        elif f == "F":
            if t == "C":
                res = (temp - 32) * 5/9
            elif t == "K":
                res = (temp - 32) * 5/9 + 273.15
            else:
                res = temp
        elif f == "K":
            if t == "C":
                res = temp - 273.15
            elif t == "F":
                res = (temp - 273.15) * 9/5 + 32
            else:
                res = temp
        if res is not None:
            st.success(f"{temp} {f} = {res:.2f} {t}")
        else:
            st.error("❌ Unsupported temperature unit!")
