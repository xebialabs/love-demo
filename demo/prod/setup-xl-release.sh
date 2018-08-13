#!/bin/bash

XLR_URL=http://localhost:15516
XLR_AUTH=admin:3dm2n

echo -n "Creating user kate... "
curl --user $XLR_AUTH $XLR_URL/users -H 'Content-Type: application/json'  --data-binary '{"username":"kate","email":"kate@company.com","fullName":"Kate Developer","password":"k3t3","loginAllowed":true}'
echo

echo -n "Creating folder Food... "
curl --user $XLR_AUTH $XLR_URL/api/v1/folders/Applications -H 'Content-Type: application/json' --data-binary '{"id":"","title":"Food","type":"xlrelease.Folder"}'
echo

echo -n "Creating global role REST-o-rant Developers... "
curl --user $XLR_AUTH $XLR_URL/roles/principals -X PUT -H 'Content-Type: application/json' --data-binary '[{"role":{"id":-1,"name":"REST-o-rant Developers"},"principals":[{"username":"kate","fullName":"Kate Developer"}]}]'
echo

echo "Granting global role \"REST-o-rant Developers\" the same permissions on folder Food as user \"XL Release Administrator\":"

echo -n "  Retrieving ID for folder Food... "
FOOD_FOLDER_ID=$(curl --user $XLR_AUTH "$XLR_URL/api/v1/folders/list?depth=10&permissions=true&resultsPerPage=1000000" -H 'Accept: application/json' -s | jq '.[] | select(.title == "Food") | .id' -r | sed 's/^Applications\///')
echo

echo -n "  Retrieving teams and permissions for folder Food..."
FOOD_FOLDER_TEAMS_AND_PERMISSIONS=$(curl --user $XLR_AUTH "$XLR_URL/teams/$FOOD_FOLDER_ID" -s)
echo

#
UPDATED_FOOD_FOLDER_TEAMS_AND_PERMISSIONS=$(echo $FOOD_FOLDER_TEAMS_AND_PERMISSIONS | sed -e 's/\("name":"admin","fullName":"XL Release Administrator","type":"PRINCIPAL"\)/\1},{"name":"REST-o-rant Developers","fullName":"REST-o-rant Developers","type":"ROLE"/g')

echo -n "  Saving teams and permissions for folder Food... "
curl --user $XLR_AUTH "$XLR_URL/teams/$FOOD_FOLDER_ID" -H 'Content-Type: application/json' --data-binary "$UPDATED_FOOD_FOLDER_TEAMS_AND_PERMISSIONS" -s > /dev/null
echo
