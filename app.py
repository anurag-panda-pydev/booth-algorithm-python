import streamlit as st
import pandas as pd

# --- Helper Functions ---
def to_binary(n, bits=4):
    """Convert integer to two's complement binary string."""
    if n < 0:
        n = (1 << bits) + n
    return format(n, f'0{bits}b')

def to_int(bin_str):
    """Convert two's complement binary string to integer."""
    bits = len(bin_str)
    val = int(bin_str, 2)
    if val >= 2 ** (bits - 1):
        val -= 2 ** bits
    return val

def booth_algorithm_table(m, r):
    bits = 4
    table_data = []

    m_bin = to_binary(m, bits)
    r_bin = to_binary(r, bits)

    A = m_bin + "0" * (bits + 1)
    S = to_binary(-m, bits) + "0" * (bits + 1)
    P = "0" * bits + r_bin + "0"  # initial product + Q-1

    table_data.append({
        "Step": "Initial",
        "A (bin)": A,
        "S (bin)": S,
        "P Register (bin)": P,
        "Last 2 bits": P[-2:],
        "Operation": "Initial Load",
        "P after Op": P,
        "P after Shift": P
    })

    for step in range(1, bits + 1):
        operation = "No Operation"
        before_op = P

        # Check last two bits
        last_two = P[-2:]
        if last_two == "01":
            P_op = bin(int(P, 2) + int(A, 2))[2:].zfill(len(P))
            operation = f"P = P + A ({P} + {A})"
        elif last_two == "10":
            P_op = bin(int(P, 2) + int(S, 2))[2:].zfill(len(P))
            operation = f"P = P + S ({P} + {S})"
        else:
            P_op = P

        # Arithmetic right shift
        sign_bit = P_op[0]
        P_shift = sign_bit + P_op[:-1]

        table_data.append({
            "Step": step,
            "A (bin)": A,
            "S (bin)": S,
            "P Register (bin)": before_op,
            "Last 2 bits": last_two,
            "Operation": operation,
            "P after Op": P_op,
            "P after Shift": P_shift
        })

        P = P_shift

    product_bin = P[:bits*2]
    product = to_int(product_bin)
    return pd.DataFrame(table_data), product, product_bin


# --- Streamlit UI ---
st.title("Booth's Algorithm Simulator (4-bit Two's Complement)")
st.markdown("Multiply two signed integers (-8 to +7) using Booth's Algorithm with step-by-step table.")

m = st.number_input("Enter Multiplicand (M):", min_value=-8, max_value=7, value=3)
r = st.number_input("Enter Multiplier (R):", min_value=-8, max_value=7, value=-4)

if st.button("Run Booth's Algorithm"):
    table, product, product_bin = booth_algorithm_table(m, r)

    st.subheader("Step-by-Step Table:")
    st.dataframe(table, use_container_width=True)

    st.subheader("Final Product:")
    st.write(f"*Decimal:* {m} × {r} = {product}")
    st.write(f"*Binary (8-bit):* {product_bin}")
    st.write(f"*Breakdown:*")
    st.write(f"A (Multiplicand): {to_binary(m, 4)}")
    st.write(f"S (-Multiplicand): {to_binary(-m, 4)}")
    st.write(f"R (Multiplier): {to_binary(r, 4)}")