class FoodInfo:
    def __init__(self):
        self.food_info = {
            "Apple": {
                "category": "Fruit",
                "serving_size": "1 medium",
                "calories": 95,
                "key_nutrients": {
                    "Carbohydrates": "25g",
                    "Protein": "0.5g",
                    "Fat": "0.2g",
                    "Fiber": "4g",
                    "Vitamins": "Vitamin C, Vitamin K",
                    "Minerals": "Potassium"
                }
            },
            "Banana": {
                "category": "Fruit",
                "serving_size": "1 medium",
                "calories": 110,
                "key_nutrients": {
                    "Carbohydrates": "27g",
                    "Protein": "1g",
                    "Fat": "0.2g",
                    "Fiber": "3g",
                    "Vitamins": "Vitamin B6, Vitamin C",
                    "Minerals": "Potassium"
                }
            },
            "Chicken Breast": {
                "category": "Protein",
                "serving_size": "3 oz cooked",
                "calories": 140,
                "key_nutrients": {
                    "Carbohydrates": "0g",
                    "Protein": "30g",
                    "Fat": "3g",
                    "Vitamins": "B Vitamins",
                    "Minerals": "Selenium, Phosphorus"
                }
            },
            "Egg": {
                "category": "Protein",
                "serving_size": "1 large",
                "calories": 70,
                "key_nutrients": {
                    "Carbohydrates": "1g",
                    "Protein": "6g",
                    "Fat": "5g",
                    "Vitamins": "Vitamin D, Vitamin B12",
                    "Minerals": "Choline"
                }
            },
            "Milk": {
                "category": "Dairy",
                "serving_size": "1 cup",
                "calories": 120,
                "key_nutrients": {
                    "Carbohydrates": "12g",
                    "Protein": "8g",
                    "Fat": "5g",
                    "Vitamins": "Vitamin D, Vitamin B12",
                    "Minerals": "Calcium, Phosphorus"
                }
            },
            "Bread": {
                "category": "Grains",
                "serving_size": "1 slice",
                "calories": 70,
                "key_nutrients": {
                    "Carbohydrates": "13g",
                    "Protein": "2g",
                    "Fat": "1g",
                    "Fiber": "1g",
                    "Vitamins": "B Vitamins",
                    "Minerals": "Iron"
                }
            },
            "Carrots": {
                "category": "Vegetable",
                "serving_size": "1 cup, chopped",
                "calories": 40,
                "key_nutrients": {
                    "Carbohydrates": "10g",
                    "Protein": "1g",
                    "Fat": "0.2g",
                    "Fiber": "2g",
                    "Vitamins": "Vitamin A, Vitamin K",
                    "Minerals": "Potassium"
                }
            }
        }

    def print_food_info(self, food_name):
        food_name = food_name.title()
        if food_name in self.food_info:
            info = self.food_info[food_name]
            print(f"Nutritional Information for {food_name} ({info['category']})")
            print(f"Serving Size: {info['serving_size']}")
            print(f"Calories: {info['calories']} kcal")
            print("Key Nutrients:")
            for nutrient, value in info["key_nutrients"].items():
                print(f"  - {nutrient}: {value}")
        else:
            print(f"No information found for {food_name}")

if __name__ == "__main__":
    food_info = FoodInfo()
    food_name = input("Enter a food name: ")
    food_info.print_food_info(food_name)
