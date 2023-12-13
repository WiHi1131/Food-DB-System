document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('addFoodButton').addEventListener('click', function() {
        var errorMessage = '';
        var foodName = document.getElementById('foodName').value;
        if (!foodName || !isNaN(foodName)) {
            errorMessage += 'Please enter a valid food name.<br>';
        }

        // Check other inputs for real numbers
        var inputs = document.querySelectorAll('.input-field');
        inputs.forEach(function(input) {
            if (input.id !== 'foodName') {
                if (input.value !== '' && isNaN(input.value)) {
                    errorMessage += `Please enter a valid number for ${input.placeholder}.<br>`;
                }
            }
        });

        if (errorMessage) {
            document.getElementById('error').innerHTML = errorMessage;
        } else {
            document.getElementById('addFoodForm').submit();
        }
    });
});