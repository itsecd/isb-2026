import argparse
import sys
from backend import Auth
from app import run_gui

def main():
    parser = argparse.ArgumentParser(description="User Authentication System")
    parser.add_argument('--mode', choices=['gui', 'cli-demo'], default='gui')
    parser.add_argument('--demo-pass', default="123")
    
    args = parser.parse_args()
    auth = Auth()
    
    match args.mode:
        case 'gui':
            run_gui(auth)
            
        case 'cli-demo':
            test_pass = args.demo_pass
            
            with auth.db.connection() as conn:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM users WHERE username = 'victim'")
                conn.commit()
                
            try:
                auth.unsafe_registration("victim", test_pass)
            except Exception as e:
                print(f"Registration error: {e}")
                
            userdata = auth.db.fetch_user("victim")
            captured_hash = userdata[0]
            
            print(f"Hash from vulnerable DB (no salt): {captured_hash}")
            found = auth.bruteforce(captured_hash)
            
            if found:
                print(f"\n[SUCCESS] Password recovered: {found}")
            else:
                print("\n[INFO] Password not found within iteration limit.")
                
        case _:
            print("Unknown execution mode.")
            
    auth.close()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(0)
    except Exception as e:
        sys.exit(1)