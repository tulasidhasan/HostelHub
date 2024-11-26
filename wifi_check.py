import subprocess
import re

def is_connected_to_wifi(target_ssid, min_signal_strength=-60):
    try:
        
        result = subprocess.check_output(["netsh", "WLAN", "show", "interfaces"], shell=True).decode('utf-8')
        
        
        if target_ssid in result:
            print(f"Connected to {target_ssid}")
            
            # Extract RSSI (signal strength) using regex.
            rssi_match = re.search(r"Signal\s*:\s*(\d+)%", result)
            if rssi_match:
                # Convert percentage to dBm (approximation)
                signal_strength = int(rssi_match.group(1)) - 100
                print(f"Current Wi-Fi signal strength: {signal_strength} dBm")
                
                # Check if the signal strength meets the proximity threshold.
                if signal_strength >= min_signal_strength:
                    print(f"Within acceptable range for {target_ssid}")
                    return True
                else:
                    print(f"Signal strength too weak for {target_ssid}")
                    return False
            else:
                print("Could not determine signal strength.")
                return False
        else:
            print(f"Not connected to {target_ssid}")
            return False
    except subprocess.CalledProcessError:
        print("Error checking Wi-Fi connection")
        return False
