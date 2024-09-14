shares_data = [
    {
        "confidence": 5
    },
{
        "confidence": 7
    },
{
        "confidence": 1
    }
]

# Sort the shares by confidence in descending order
sorted_shares = sorted(shares_data, key=lambda x: x.get("confidence", 0), reverse=True)

print(sorted_shares)