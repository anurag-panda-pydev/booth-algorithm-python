from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text

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
    console = Console()
    
    # Convert to 4-bit 2's complement
    M = to_4bit_twos_complement(multiplicand)
    Q = to_4bit_twos_complement(multiplier)
    neg_M = to_4bit_twos_complement(-multiplicand)

    # Rich panels for initial values
    console.print(Panel.fit(f"[bold]Booth's Algorithm: {multiplicand} x {multiplier}[/bold]", style="cyan"))
    console.print(f"[bold]Multiplicand (M):[/bold] {multiplicand} → [green]{M}[/green]")
    console.print(f"[bold]Multiplier (Q):[/bold] {multiplier} → [green]{Q}[/green]")
    console.print(f"[bold]-M:[/bold] {neg_M} ({-multiplicand})\n")

    # Initialize registers
    # A (accumulator) - 4 bits, initially 0
    A = "0000"
    # Q (multiplier) - 4 bits
    # Q₋₁ (extra bit) - 1 bit, initially 0
    Q_minus_1 = "0"
    n = 4
    step = 0

    table = Table(title="Step-by-step Execution", show_lines=True)
    table.add_column("Step", justify="center")
    table.add_column("A", justify="center")
    table.add_column("Q", justify="center")
    table.add_column("Q₋₁", justify="center")
    table.add_column("Q₀Q₋₁", justify="center")
    table.add_column("Action", justify="left")
    table.add_column("After Shift", justify="center")

    for i in range(n):
        step += 1
        Q0 = Q[-1]
        Q0Q_minus_1 = Q0 + Q_minus_1

        action = ""
        before_A = A
        before_Q = Q
        before_Qm1 = Q_minus_1

        if Q0Q_minus_1 == "10":
            action = "[red]A = A - M[/red]"
            A_int = int(A, 2)
            neg_M_int = int(neg_M, 2)
            result = (A_int + neg_M_int) & 0xF
            A = format(result, '04b')
        elif Q0Q_minus_1 == "01":
            action = "[green]A = A + M[/green]"
            A_int = int(A, 2)
            M_int = int(M, 2)
            result = (A_int + M_int) & 0xF
            A = format(result, '04b')
        else:
            action = "[yellow]No operation[/yellow]"

        # Arithmetic right shift
        sign_bit = A[0]
        new_Q_minus_1 = Q[-1]
        new_Q = A[-1] + Q[:-1]
        new_A = sign_bit + A[:-1]

        after_shift = f"{new_A} {new_Q} {new_Q_minus_1}"

        table.add_row(
            str(step),
            before_A,
            before_Q,
            before_Qm1,
            Q0Q_minus_1,
            action,
            after_shift
        )

        A = new_A
        Q = new_Q
        Q_minus_1 = new_Q_minus_1

    final_result_binary = A + Q
    if final_result_binary[0] == '1':
        inverted = ''.join('1' if bit == '0' else '0' for bit in final_result_binary)
        decimal_result = -((int(inverted, 2) + 1) & 0xFF)
    else:
        decimal_result = int(final_result_binary, 2)

    console.print(table)
    console.print(Panel.fit(
        f"[bold]Final result:[/bold]\n"
        f"Binary: [yellow]{A}{Q}[/yellow] ([cyan]{A}[/cyan] [magenta]{Q}[/magenta])\n"
        f"Decimal: [green]{decimal_result}[/green]\n"
        f"Verification: {multiplicand} × {multiplier} = {multiplicand * multiplier}",
        style="green"
    ))

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