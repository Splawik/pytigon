# Set the CREDENTIAL variable to the result of the script execution: 1_rest_gen_credential.py
export CREDENTIAL=cmNoZDkwYjBIOUllVzNJV05TNGl6eEFhNUFpOUlGc21yeUtOeFNrbDo2UHAyMGNDd2ZaVTNxYWlYSnVYZVE2TUdpU1hQTGtCZThBSHZKZWVqMFUyWlBZWlV3MER5c0pIUWhmZkhrWmdBQzlUeGVPb3M3eHhoSGw0czU3UldYNVFIN3hyOWJoSnNKQnVKdEFQUEIzb1JYa2lWbEdIcDRSZGxKVXVlWFppUA==

curl -X POST -H "Authorization: Basic ${CREDENTIAL}" -H "Cache-Control: no-cache" -H "Content-Type: application/x-www-form-urlencoded" "http://127.0.0.1:8000/o/token/" -d "grant_type=client_credentials"
