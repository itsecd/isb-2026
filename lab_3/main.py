from incription import *
from decription import *
from keys_generation import *
import warnings
from cryptography.utils import CryptographyDeprecationWarning
warnings.filterwarnings("ignore", category=CryptographyDeprecationWarning)


def main():
    config = load_config('settings.json')
    if not config:
        return

    while True:
        print("\n--- Hybrid cryptosystem ---")
        print("1. Key generation (frist scenario)")
        print("2. Data encryption (second scenerio)")
        print("3. Data decryption (third scenerio)")
        print("0. Exit")
        
        choice = input("Choose the scenerio: ")
        
        if choice == '1':
            while True:
                try:
                  
                    key_size = int(input("Please, enter key size (64, 128, 192 bits): "))
                    if key_size in [64, 128, 192]:
                        break
                    print("Error: please enter 64, 128, or 192")
                except ValueError:
                    print("Error: please enter a valid number")
            
        
            triple_des_key_generation(key_size // 8, config)
            
            for username in config['users']:
                print(f"\n--- Generating keys for {username} ---")
            
                rsa_key_generation(config, username)
                
                encrypt_session_key_for_user(config, username)
                
            print("\nFirst scenario is completed for all users.")

        elif choice == '2':
            username = input("User_name (whose closed key will be used, Bob, for example): ")
            input_file = config['files']['initial']
            encrypted_file = config['files']['incrypted'] 
            
            try:
                decrypted_session_key = session_key_decryption(config, username)
                encrypt_file_3des(input_file, encrypted_file, decrypted_session_key)
                print("second scenario is completed.")
            except Exception as e:
                print(f"Error during encryption: {e}")

        elif choice == '3':
            username = input("User_name (whose closed key will be used, Alice, for example): ")
            encrypted_file = config['files']['incrypted']
            decrypted_file = config['files']['decrypted']
            
            try:
                decrypted_session_key = session_key_decryption(config, username)
                decrypt_file_3des(encrypted_file, decrypted_file, decrypted_session_key)
                print("third scenario is completed.")
            except Exception as e:
                print(f"Error during decryption: {e}")

        elif choice == '0':
            print("Exit...")
            break
        else:
            print("Wrong mode, enter again.")

if __name__ == "__main__":
    main()

