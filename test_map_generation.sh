#!/bin/bash

# Test if the map generation endpoint is working fast
echo "Testing map generation endpoint response time..."

for i in {1..3}; do
    echo ""
    echo "Attempt $i:"
    start=$(date +%s%N)
    
    response=$(curl -s -w "\nHTTP_STATUS:%{http_code}" -X POST "http://localhost:10000/api/maps/generate" \
        -H "Content-Type: application/json" \
        -d "{
            \"owner_id\": 100,
            \"owner_name\": \"testuser\",
            \"map_id\": \"test_map_$i\",
            \"width\": 20,
            \"height\": 20
        }")
    
    end=$(date +%s%N)
    elapsed=$(( (end - start) / 1000000 ))
    
    echo "Response time: ${elapsed}ms"
    
    # Extract HTTP status
    status=$(echo "$response" | grep "HTTP_STATUS" | cut -d: -f2)
    echo "HTTP Status: $status"
    
    if [ "$status" != "201" ]; then
        echo "Failed response:"
        echo "$response" | head -c 200
    fi
done

