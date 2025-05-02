document.getElementById("property-form").addEventListener("submit", async function(event) {
    event.preventDefault();
    
    const area = document.getElementById("area").value;
    const bedroom = document.getElementById("bedroom").value;
    const bathroom = document.getElementById("bathroom").value;
    const location = document.getElementById("location").value;

    const response = await fetch("/predict", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            area_sqft: area,
            bedroom: bedroom,
            bathroom: bathroom,
            location: location
        })
    });

    const data = await response.json();
    
    if (data.success) {
        document.getElementById("results").style.display = "block";
        document.getElementById("rent-price").innerHTML = `Rent Price: ${data.rent_price} BDT`;
        document.getElementById("sell-price").innerHTML = `Sell Price: ${data.sell_price} BDT`;
        document.getElementById("inflation").innerHTML = `Inflation: ${data.inflation}%`;
    } else {
        alert("Error: Unable to fetch prediction");
    }
});
