<!doctype html>
<html lang="en" data-bs-theme="dark">

<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>GT7 Used Car Info</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-KK94CHFLLe+nY2dmCWGMq91rCGa5gtU4mk92HdvYe+M/SXH301p5ILy+dN9+nJOZ" crossorigin="anonymous">
</head>

<body>
    <div class="container">
        <header class="d-flex flex-wrap justify-content-center py-3 mb-4 border-bottom">
            <h1 style="text-align: center;">GT7 Used Car Info</h1>
        </header>
    </div>


    <div class="accordion container" id="accordionExample">
        {% for oneData in data %}
        <div class="accordion-item">
            <h2 class="accordion-header">
                <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#collapse{{oneData.date}}" aria-expanded="true" aria-controls="collapse{{oneData.date}}">
                    {{oneData.date}}
                </button>
            </h2>
            {% if loop.index == 1%}
            <div id="collapse{{oneData.date}}" class="accordion-collapse collapse show" data-bs-parent="#accordionExample">
                {% else %}
                <div id="collapse{{oneData.date}}" class="accordion-collapse collapse" data-bs-parent="#accordionExample">
                    {% endif %}

                    <div class="accordion-body">
                        <h2 style="text-align: center;">Used Car Dealership</h2>
                        <table class="table">
                            <thead>
                                <tr>
                                    <th scope="col">Maker</th>
                                    <th scope="col">Car</th>
                                    <th scope="col">Price</th>
                                </tr>
                            </thead>
                            <tbody>
                                {% for car in oneData.list_used %}
                                {% if car.isOld == True %}
                                <tr class="table-danger">
                                    {% elif car.isOld == False %}
                                <tr>
                                    {% else %}
                                <tr class="table-warning">
                                    {% endif %}
                                    <td>{{car.makername}}</td>
                                    <th>{{car.carname}}</th>
                                    <td>{{car.price_in_jpy}}</td>
                                </tr>
                                {% endfor %}
                                {% if oneData.list_legend == [] %}
                                <td colspan="3" style="text-align: center;">No new cars available.</td>
                                {% endif %}
                            </tbody>
                        </table>

                        <br><br>
                        <h2 style="text-align: center;">Legendary Dealership</h2>
                        <table class="table">
                            <thead>
                                <tr>
                                    <th scope="col">Maker</th>
                                    <th scope="col">Car</th>
                                    <th scope="col">Price</th>
                                </tr>
                            </thead>
                            <tbody>
                                {% for car in oneData.list_legend %}
                                {% if car.isOld == True %}
                                <tr class="table-danger">
                                    {% elif car.isOld == False %}
                                <tr>
                                    {% else %}
                                <tr class="table-warning">
                                    {% endif %}
                                    <td>{{car.makername}}</td>
                                    <th>{{car.carname}}</th>
                                    <td style="text-align: right;">{{car.price_in_jpy}}</td>
                                </tr>
                                {% endfor %}
                                {% if oneData.list_legend == [] %}
                                <td colspan="3" style="text-align: center;">No new cars available.</td>
                                {% endif %}
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>
            {% endfor %}
        </div>
        <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha3/dist/js/bootstrap.bundle.min.js" integrity="sha384-ENjdO4Dr2bkBIFxQpeoTz1HIcje39Wm4jDKdf19U8gI4ddQ3GYNS7NTKfAdVQSZe" crossorigin="anonymous"></script>
</body>

</html>
