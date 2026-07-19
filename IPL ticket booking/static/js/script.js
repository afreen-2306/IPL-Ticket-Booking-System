const seats = document.querySelectorAll(".seat-btn");
const hiddenSeat = document.getElementById("seat_number");
const quantity = document.getElementById("quantity");

const selectedSeatsText = document.getElementById("selectedSeats");
const ticketCount = document.getElementById("ticketCount");
const totalPrice = document.getElementById("totalPrice");

const category = document.querySelector("select[name='seat_category']");

let selectedSeats = [];

// Disable all seats initially
seats.forEach(seat => seat.style.display = "none");

// Show seats according to category
category.addEventListener("change", function () {

    selectedSeats = [];
    hiddenSeat.value = "";
    quantity.value = 0;

    selectedSeatsText.innerHTML = "None";
    ticketCount.innerHTML = "0";
    totalPrice.innerHTML = "₹0";

    seats.forEach(seat => {

        seat.classList.remove("selected-seat");

        const seatNo = seat.dataset.seat;

        if (this.value == "Business") {

            seat.style.display = seatNo.startsWith("A") ? "inline-block" : "none";

        }

        else if (this.value == "Premium") {

            seat.style.display = seatNo.startsWith("B") ? "inline-block" : "none";

        }

        else if (this.value == "Standard") {

            seat.style.display = seatNo.startsWith("C") ? "inline-block" : "none";

        }

        else {

            seat.style.display = "none";

        }

    });

});

// Seat click
seats.forEach(seat => {

    seat.addEventListener("click", function () {

        const seatNo = this.dataset.seat;

        if (selectedSeats.includes(seatNo)) {

            selectedSeats = selectedSeats.filter(s => s !== seatNo);
            this.classList.remove("selected-seat");

        } else {

            selectedSeats.push(seatNo);
            this.classList.add("selected-seat");

        }

        hiddenSeat.value = selectedSeats.join(",");
        quantity.value = selectedSeats.length;

        selectedSeatsText.innerHTML =
            selectedSeats.length ? selectedSeats.join(", ") : "None";

        ticketCount.innerHTML = selectedSeats.length;

        let price = 0;

        if (category.value == "Business")
            price = 3000;
        else if (category.value == "Premium")
            price = 2000;
        else if (category.value == "Standard")
            price = 1000;

        totalPrice.innerHTML = "₹" + (selectedSeats.length * price);

    });

});