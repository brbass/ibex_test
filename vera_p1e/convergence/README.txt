Several types of meshes are used.

scaled_pincell_N: A pincell with N points across the clad, 3N points across the radius of the fuel and 8N points across the length of the moderator. This results in approximately 1/2 spacing for points in the fuel and 2/5 in the moderator compared to the clad.

uniform_pincell_N: A more uniform pincell with N points across the clad, 6N points across the radius of the fuel and 16N points across the length of the moderator. This results in approximately (16N)^2 total points. 

square_N: A pincell with 16N points across the length of the moderator. This results in exactly (16N)^2 points. 
