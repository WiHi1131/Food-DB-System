document.addEventListener('DOMContentLoaded', function() {
    var searchInput = document.getElementById('searchInput');
    var suggestionsContainer = document.getElementById('suggestions-container');

    searchInput.addEventListener('input', function() {
        var searchTerm = searchInput.value;

        if (searchTerm.length > 0) {
            fetch('/get_food_suggestions?term=' + encodeURIComponent(searchTerm))
                .then(response => response.json())
                .then(data => {
                    // Clear any existing suggestions
                    removeAllChildNodes(suggestionsContainer);

                    if (data.length > 0) {
                        // Create a new list of suggestions
                        var suggestionList = document.createElement('ul');
                        data.forEach(function(item) {
                            var listItem = document.createElement('li');
                            listItem.textContent = item;
                            listItem.addEventListener('click', function() {
                                fetchFoodInfo(item);
                            });
                            suggestionList.appendChild(listItem);
                        });
                        suggestionsContainer.appendChild(suggestionList);
                    } else {
                        // Display a message if no suggestions are found
                        var noResultsMsg = document.createElement('div');
                        noResultsMsg.textContent = `No foods named '${searchTerm}' in the database`;
                        suggestionsContainer.appendChild(noResultsMsg);
                    }
                })
                .catch(error => console.error('Error:', error));
        } else {
            // Clear suggestions when there is no input
            removeAllChildNodes(suggestionsContainer);
        }
    });

    function fetchFoodInfo(foodName) {
        fetch('/get_food_info?name=' + encodeURIComponent(foodName))
            .then(response => response.json())
            .then(data => {
                if (data.error) {
                    console.error(data.error);
                } else {
                    displayFoodInfo(data);
                }
            })
            .catch(error => console.error('Error:', error));
    }

    function displayFoodInfo(info) {
        var infoContainer = document.getElementById('food-info');
        removeAllChildNodes(infoContainer);
        Object.keys(info).forEach(key => {
            var p = document.createElement('p');
            p.textContent = `${key}: ${info[key]}`;
            infoContainer.appendChild(p);
        });
    }

    function removeAllChildNodes(parent) {
        while (parent.firstChild) {
            parent.removeChild(parent.firstChild);
        }
    }
});



