from etl import is_within_city_center_radius, filter_urban_cities

# I put all the tests for each method in the same method to be quicker (ideally they each go into their own method with proper naming)
class TestEtlMethods:
    def test_filter_urban_cities(self):
        population = 6000
        population_proper = 2499
        assert filter_urban_cities(population_proper, population) == False

        population = 2499
        population_proper = 2499
        assert filter_urban_cities(population_proper, population) == False

        population = 95000
        population_proper = 50001
        assert filter_urban_cities(population_proper, population) == True

        population = 2500
        population_proper = 2500
        assert filter_urban_cities(population_proper, population) == True

        population = 45000
        population_proper = 44900
        assert filter_urban_cities(population_proper, population) == False

        population = 6000
        population_proper = 2499
        assert filter_urban_cities(population_proper, population) == False

        population = 50000
        population_proper = 50000
        assert filter_urban_cities(population_proper, population) == True

        population = 51000
        population_proper = 50000
        assert filter_urban_cities(population_proper, population) == False

    def test_is_within_city_center_radius(self):
        assert is_within_city_center_radius(12.5, 12.4) == True
        assert is_within_city_center_radius(12.4, 12.5) == True
        assert is_within_city_center_radius(12.4, 12.4) == True
        assert is_within_city_center_radius(12.6, 12.4) == False