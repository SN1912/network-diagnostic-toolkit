
from diagnostics import (
    get_ip_configuration,
    get_default_gateway,
    check_internet_connection,
    check_dns_resolution,
    detect_network_problems,
    check_college_server,
    analyze_network_route,
    check_tcp_port,
    generate_diagnostic_report
)


# Store diagnostic results
results = {}


# ==========================================
# DISPLAY MENU
# ==========================================

def display_menu():

    print("\n" + "=" * 55)
    print("          NETWORK DIAGNOSTIC TOOLKIT")
    print("=" * 55)

    print("\n1.  Check IP Configuration")
    print("2.  Check Default Gateway")
    print("3.  Test Internet Connectivity")
    print("4.  Test DNS Resolution")
    print("5.  Automatic Network Diagnosis")
    print("6.  Check College Server")
    print("7.  Generate Diagnostic Report")
    print("8.  Analyze Network Route")
    print("9.  Test TCP Port Connectivity")
    print("0.  Exit")

    print("=" * 55)


# ==========================================
# MAIN PROGRAM
# ==========================================

def main():

    while True:

        display_menu()

        choice = input(
            "\nEnter your choice: "
        ).strip()

        if choice == "1":

            results["IP Configuration"] = (
                get_ip_configuration()
            )

        elif choice == "2":

            results["Default Gateway"] = (
                get_default_gateway()
            )

        elif choice == "3":

            results["Internet Connectivity"] = (
                check_internet_connection()
            )

        elif choice == "4":

            results["DNS Resolution"] = (
                check_dns_resolution()
            )

        elif choice == "5":

            results["Automatic Diagnosis"] = (
                detect_network_problems()
            )

        elif choice == "6":

            results["College Server"] = (
                check_college_server()
            )

        elif choice == "7":

            if results:
                generate_diagnostic_report(results)

            else:
                print(
                    "\nNo diagnostic results available. "
                    "Run a test first."
                )

        elif choice == "8":

            results["Network Route"] = (
                analyze_network_route()
            )

        elif choice == "9":

            results["TCP Port Test"] = (
                check_tcp_port()
            )

        elif choice == "0":

            print(
                "\nThank you for using "
                "Network Diagnostic Toolkit!"
            )

            break

        else:

            print(
                "\nInvalid choice! Please try again."
            )


# ==========================================
# PROGRAM ENTRY POINT
# ==========================================

if __name__ == "__main__":
    main()
