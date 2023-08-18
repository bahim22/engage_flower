curl -v -u $user@$FS_URL:$FS_API_KEY -H "Content-Type: application/json" -d '{ "description": "Details about the issue...", "subject": "Support Needed...", "email": "user0@domain" "priority": 1, "status": 2, "cc_emails": ["user1@domain" "user2@domain"], "workspace_id": 3 }' -X POST '$FS_URL/tickets'

curl -v -u api-key:$FS_KEY -X GET '$FS_URL/agents?active=true'

curl -v -u api.user@ministryofmagic.govhogwarts.edu:test -X GET '$FS_URL/departments'

curl - v - u ibalde@pointpark.freshservice.com: $FS_API_KEY - X GET'$FS_URL/agents?active=true'

curl -v -u  -X "Connection: close" $FS_URL