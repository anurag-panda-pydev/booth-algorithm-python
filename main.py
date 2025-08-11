def to_4bit_twos_complement(num):
    """Convert a signed integer (-8 to +7) to 4-bit 2's complement binary string."""
    if num < -8 or num > 7:
        raise ValueError("Number must be in range -8 to 7")
    
    if num >= 0:
        binary = format(num, '04b')
    else:
        #negative numbers: 2's complement
        #Step 1: Get binary of absolute value
        abs_binary = format(abs(num), '04b')
        #Step 2: Invert the bits
        inverted = ''.join('1' if bit == '0' else '0' for bit in abs_binary)
        #Step 3: Add 1
        inverted_int = int(inverted, 2)
        twos_comp = (inverted_int + 1) & 0xF #keep only 4 bits
        binary = format(twos_comp, '04b')
        
    return binary

def sign_extend(binary_str, target_length):
    """Sign extend a binary string to target length"""
    sign_bit = binary_str[0]
    extension_bits = sign_bit * (target_length - len(binary_str))
    return extension_bits + binary_str

def booth_algorithm(multiplicand, multiplier):
    """
    Implement Booth's Algorithm for multiplication.
    Returns the step-by-step process and final result.
    """
    print(f"\n=== Booth's Algorithm: {multiplicand} x {multiplier} ===")
    
    # Convert to 4-bit 2's complement
    M = to_4bit_twos_complement(multiplicand)
    Q = to_4bit_twos_complement(multiplier)
    
    print(f"Multiplicand (M): {multiplicand} → {M}")
    print(f"Multiplier (Q): {multiplier} → {Q}")
    
    # Initialize registers
    # A (accumulator) - 4 bits, initially 0
    A = "0000"
    # Q (multiplier) - 4 bits
    # Q₋₁ (extra bit) - 1 bit, initially 0
    Q_minus_1 = "0"
    
    # -M (negative of multiplicand)
    neg_M = to_4bit_twos_complement(-multiplicand)
    
    print(f"\nInitial setup:")
    print(f"M = {M} ({multiplicand})")
    print(f"-M = {neg_M} ({-multiplicand})")
    print(f"A = {A}")
    print(f"Q = {Q}")
    print(f"Q₋₁ = {Q_minus_1}")
    
    print(f"\nStep-by-step execution:")
    print("Step | A    | Q    | Q₋₁ | Q₀Q₋₁ | Action")
    print("-" * 45)
    
    n = 4  # 4-bit numbers
    step = 0
    
    for i in range(n):
        step += 1
        Q0 = Q[-1]  # Least significant bit of Q
        Q0Q_minus_1 = Q0 + Q_minus_1
        
        print(f"{step:4} | {A} | {Q} | {Q_minus_1:3} | {Q0Q_minus_1:5} | ", end="")
        
        # Booth's algorithm decision
        if Q0Q_minus_1 == "10":
            # Subtract M from A (add -M)
            print("A = A - M")
            A_int = int(A, 2)
            neg_M_int = int(neg_M, 2)
            result = (A_int + neg_M_int) & 0xF  # Keep 4 bits
            A = format(result, '04b')
        elif Q0Q_minus_1 == "01":
            # Add M to A
            print("A = A + M")
            A_int = int(A, 2)
            M_int = int(M, 2)
            result = (A_int + M_int) & 0xF  # Keep 4 bits
            A = format(result, '04b')
        else:
            print("No operation")
        
        # Arithmetic right shift of A and Q
        # Save the sign bit of A
        sign_bit = A[0]
        # Shift A right, Q₋₁ gets Q[0], Q gets A[3]
        new_Q_minus_1 = Q[-1]
        new_Q = A[-1] + Q[:-1]
        new_A = sign_bit + A[:-1]  # Arithmetic right shift (preserve sign)
        
        A = new_A
        Q = new_Q
        Q_minus_1 = new_Q_minus_1
        
        print(f"     | {A} | {Q} | {Q_minus_1:3} |       | After shift")
    
    # Combine A and Q for final result (8-bit result)
    final_result_binary = A + Q
    
    # Convert to decimal (8-bit signed)
    if final_result_binary[0] == '1':  # Negative number
        # Convert from 2's complement
        inverted = ''.join('1' if bit == '0' else '0' for bit in final_result_binary)
        decimal_result = -((int(inverted, 2) + 1) & 0xFF)
    else:
        decimal_result = int(final_result_binary, 2)
    
    print(f"\nFinal result:")
    print(f"Binary: {A}{Q} ({A} {Q})")
    print(f"Decimal: {decimal_result}")
    print(f"Verification: {multiplicand} × {multiplier} = {multiplicand * multiplier}")
    
    return decimal_result

def main():
    """Main function to get user input and perform Booth's multiplication."""
    print("Booth's Algorithm for Signed Integer Multiplication")
    print("Valid range: -8 to +7")
    print("=" * 50)
    
    try:
        # Get user input
        multiplicand = int(input("Enter first number (multiplicand): "))
        multiplier = int(input("Enter second number (multiplier): "))
        
        # Validate range
        if multiplicand < -8 or multiplicand > 7:
            print("Error: Multiplicand must be in range -8 to +7")
            return
        
        if multiplier < -8 or multiplier > 7:
            print("Error: Multiplier must be in range -8 to +7")
            return
        
        # Perform Booth's multiplication
        result = booth_algorithm(multiplicand, multiplier)
        
        print(f"\n{'='*50}")
        print(f"Final Answer: {multiplicand} × {multiplier} = {result}")
        
    except ValueError as e:
        print(f"Error: {e}")
    except KeyboardInterrupt:
        print("\nProgram interrupted by user.")

if __name__ == "__main__":
    main()