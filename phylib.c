//Phylib.c File

#include "phylib.h"
#include <stdlib.h>
#include <stdio.h>
#include <math.h>
#include <string.h>

// Global Hole Coordinates
phylib_coord topLeft = {0.0, 0.0};                 // Top-left hole
phylib_coord midLeft = {0.0, PHYLIB_TABLE_WIDTH};  // Middle-left hole
phylib_coord botLeft = {0.0, PHYLIB_TABLE_LENGTH}; // Bottom-left hole

phylib_coord topRight = {PHYLIB_TABLE_WIDTH, 0.0};                 // Top-right hole
phylib_coord botRight = {PHYLIB_TABLE_WIDTH, PHYLIB_TABLE_LENGTH}; // Bottom-right hole
phylib_coord midRight = {PHYLIB_TABLE_WIDTH, PHYLIB_TABLE_WIDTH};  // Middle-right hole

// create new still ball object
phylib_object *phylib_new_still_ball(unsigned char number, phylib_coord *pos)
{

    // allocate memory for new still ball
    phylib_object *newObj = (phylib_object *)malloc(sizeof(phylib_object));
    if (newObj == NULL)
    {
        return NULL; // Return NULL if memory allocation fails
    }

    // initialize entire struct to 0
    memset(newObj, 0, sizeof(phylib_object));

    // set object members
    newObj->type = PHYLIB_STILL_BALL;
    newObj->obj.still_ball.number = number;
    newObj->obj.still_ball.pos = *pos;

    return newObj;
}

// create new rolling ball object
phylib_object *phylib_new_rolling_ball(unsigned char number, phylib_coord *pos, phylib_coord *vel, phylib_coord *acc)
{

    // allocate memory for new still ball
    phylib_object *newObj = (phylib_object *)malloc(sizeof(phylib_object));
    if (newObj == NULL)
    {
        return NULL; // Return NULL if memory allocation fails
    }

    // initialize entire struct to 0
    memset(newObj, 0, sizeof(phylib_object));

    // set object members
    newObj->type = PHYLIB_ROLLING_BALL;
    newObj->obj.rolling_ball.number = number;
    newObj->obj.rolling_ball.pos = *pos;
    newObj->obj.rolling_ball.vel = *vel;
    newObj->obj.rolling_ball.acc = *acc;

    return newObj;
}

// create a new hole object
phylib_object *phylib_new_hole(phylib_coord *pos)
{

    // allocate memory for new hole
    phylib_object *newObj = (phylib_object *)malloc(sizeof(phylib_object));
    if (newObj == NULL)
    {
        return NULL; // Return NULL if memory allocation fails
    }

    // initialize entire struct to 0
    memset(newObj, 0, sizeof(phylib_object));

    // set object members
    newObj->type = PHYLIB_HOLE;
    newObj->obj.hole.pos = *pos;

    return newObj;
}

// create a new horizontal cushion object
phylib_object *phylib_new_hcushion(double y)
{

    // allocate memory for horizontal cushion
    phylib_object *newObj = (phylib_object *)malloc(sizeof(phylib_object));
    if (newObj == NULL)
    {
        return NULL; // Return NULL if memory allocation fails
    }

    // initialize entire struct to 0
    memset(newObj, 0, sizeof(phylib_object));

    // set object members
    newObj->type = PHYLIB_HCUSHION;
    newObj->obj.hcushion.y = y;

    return newObj;
}

// create a new verticle cushion object
phylib_object *phylib_new_vcushion(double x)
{

    // allocate memory for vertical cushion
    phylib_object *newObj = (phylib_object *)malloc(sizeof(phylib_object));
    if (newObj == NULL)
    {
        return NULL; // Return NULL if memory allocation fails
    }

    // initialize entire struct to 0
    memset(newObj, 0, sizeof(phylib_object));

    // set object members
    newObj->type = PHYLIB_VCUSHION;
    newObj->obj.vcushion.x = x;

    return newObj;
}

// create a new table table
phylib_table *phylib_new_table(void)
{
    // allocate memory for newtable
    phylib_table *newTable = (phylib_table *)malloc(sizeof(phylib_table));
    if (newTable == NULL)
    {
        return NULL; // Return NULL if memory allocation fails
    }

    // initialize entire struct to 0
    memset(newTable, 0, sizeof(phylib_object));

    // set table members
    newTable->object[0] = phylib_new_hcushion(0.0);
    newTable->object[1] = phylib_new_hcushion(PHYLIB_TABLE_LENGTH);
    newTable->object[2] = phylib_new_vcushion(0.0);
    newTable->object[3] = phylib_new_vcushion(PHYLIB_TABLE_WIDTH);
    newTable->object[4] = phylib_new_hole(&topLeft);
    newTable->object[5] = phylib_new_hole(&midLeft);
    newTable->object[6] = phylib_new_hole(&botLeft);
    newTable->object[7] = phylib_new_hole(&topRight);
    newTable->object[8] = phylib_new_hole(&midRight);
    newTable->object[9] = phylib_new_hole(&botRight);

    // set rest table object member array to null
    for (int i = 10; i < PHYLIB_MAX_OBJECTS; i++)
    {
        newTable->object[i] = NULL;
    }
    return newTable;
}

// Utility Functions

// copy and object
void phylib_copy_object(phylib_object **dest, phylib_object **src)
{

    // If source object is null set destination object to null
    if (*src == NULL)
    {
        *dest = NULL;
        return;
    }
    else
    {
        // allocate memory for destination object, return null if fails
        *dest = (phylib_object *)malloc(sizeof(phylib_object));
        if (*dest == NULL)
        {
            return; // Return if memory allocation fails
        }
    }

    // copy contents of src to dest
    memcpy(*dest, *src, sizeof(phylib_object));
}

// function makes copy of table
phylib_table *phylib_copy_table(phylib_table *table)
{
    // allocate memory for copied table, if it fails return null
    phylib_table *tableCopy = (phylib_table *)malloc(sizeof(phylib_table));
    if (tableCopy == NULL)
    {
        return NULL; // Return if memory allocation fails
    }

    // copy over table to tablecopy
    memcpy(tableCopy, table, sizeof(phylib_table)); // do I need to make a deep copy

    // deep copy, not just struct but members within
    tableCopy->time = table->time;
    for (int i = 0; i < PHYLIB_MAX_OBJECTS; i++)
    {
        if (table->object[i] != NULL) // if object is null, we're going to use copy object function to deep copy
        {
            phylib_copy_object(&(tableCopy->object[i]), &(table->object[i]));
        }
    }

    return tableCopy;
}

// function to add objects to a table
void phylib_add_object(phylib_table *table, phylib_object *object)
{

    for (int i = 0; i < PHYLIB_MAX_OBJECTS; i++) // loop through all the objects
    {
        if (table->object[i] == NULL) // if an object in table array is null, copy the object
        {
            table->object[i] = object; //<-----------------
            break;
        }
    }
}

// function to free table memory
void phylib_free_table(phylib_table *table)
{
    for (int i = 0; i < PHYLIB_MAX_OBJECTS; i++) // loop through the objects and free those first if they aren't null
    {
        if (table->object[i] != NULL)
        {
            free(table->object[i]);
            table->object[i] = NULL; // set objects in array to null
        }
    }
    free(table); // free the entire struct
}

// function to find difference of x and y coords
phylib_coord phylib_sub(phylib_coord c1, phylib_coord c2)
{

    phylib_coord coordDiff; // create new coord struct
    coordDiff.x = c1.x - c2.x;
    coordDiff.y = c1.y - c2.y;

    return coordDiff;
}

// function to find a vector
double phylib_length(phylib_coord c)
{

    double vector = sqrt((c.x * c.x) + (c.y * c.y)); // vector equation

    return vector;
}

// function to find dot product
double phylib_dot_product(phylib_coord a, phylib_coord b)
{

    double dotProduct = (a.x * b.x) + (a.y * b.y); // dot product equation

    return dotProduct;
}

// function to find distance of two objects
double phylib_distance(phylib_object *obj1, phylib_object *obj2)
{
    if (obj1->type != PHYLIB_ROLLING_BALL) // if obj1 isn't of type rolling ball
    {
        return -1.0;
    }

    double distance = 0.0; // initialize distance

    switch (obj2->type) // switch case, checking type of obj2
    {
    case PHYLIB_ROLLING_BALL: // if obj2 is a rolling ball, honestly code would be equally messy using phylib_sub
        distance = sqrt(((obj1->obj.rolling_ball.pos.x - obj2->obj.rolling_ball.pos.x) * (obj1->obj.rolling_ball.pos.x - obj2->obj.rolling_ball.pos.x)) +
                        ((obj1->obj.rolling_ball.pos.y - obj2->obj.rolling_ball.pos.y) * (obj1->obj.rolling_ball.pos.y - obj2->obj.rolling_ball.pos.y))) -
                   PHYLIB_BALL_DIAMETER;
        break;
    case PHYLIB_STILL_BALL: // if obj2 is a still ball
        distance = sqrt(((obj1->obj.rolling_ball.pos.x - obj2->obj.still_ball.pos.x) * (obj1->obj.rolling_ball.pos.x - obj2->obj.still_ball.pos.x)) +
                        ((obj1->obj.rolling_ball.pos.y - obj2->obj.still_ball.pos.y) * (obj1->obj.rolling_ball.pos.y - obj2->obj.still_ball.pos.y))) -
                   PHYLIB_BALL_DIAMETER;
        break;
    case PHYLIB_HOLE: // if obj2 is a hole
        distance = sqrt(((obj2->obj.hole.pos.x - obj1->obj.rolling_ball.pos.x) * (obj2->obj.hole.pos.x - obj1->obj.rolling_ball.pos.x)) +
                        ((obj2->obj.hole.pos.y - obj1->obj.rolling_ball.pos.y) * (obj2->obj.hole.pos.y - obj1->obj.rolling_ball.pos.y))) -
                   PHYLIB_HOLE_RADIUS;
        break;
    case PHYLIB_HCUSHION: // if obj2 is a horizontal cushion
        distance = fabs(obj1->obj.rolling_ball.pos.y - obj2->obj.hcushion.y) - PHYLIB_BALL_RADIUS;
        break;
    case PHYLIB_VCUSHION: // if obj2 is a verticle cushion
        distance = fabs(obj1->obj.rolling_ball.pos.x - obj2->obj.vcushion.x) - PHYLIB_BALL_RADIUS;
        break;
    default:
        return -1.0; // return -1.0 if none of the above
    }

    return distance;
}

// Simulation Function defintions

// function updating a ball physics after it has rolled over time
void phylib_roll(phylib_object *new, phylib_object *old, double time)
{

    if (new->type != PHYLIB_ROLLING_BALL && old->type != PHYLIB_ROLLING_BALL) // if either object is not a rolling ball, return
    {
        return;
    }

    // update pos and vel of the new ball
    new->obj.rolling_ball.pos.x = old->obj.rolling_ball.pos.x + (old->obj.rolling_ball.vel.x * time) + (0.5 * old->obj.rolling_ball.acc.x * (time * time));
    new->obj.rolling_ball.pos.y = old->obj.rolling_ball.pos.y + (old->obj.rolling_ball.vel.y * time) + (0.5 * old->obj.rolling_ball.acc.y * (time * time));

    new->obj.rolling_ball.vel.x = old->obj.rolling_ball.vel.x + (old->obj.rolling_ball.acc.x * time);
    new->obj.rolling_ball.vel.y = old->obj.rolling_ball.vel.y + (old->obj.rolling_ball.acc.y * time);

    // Check sign change, if so, update the vel and acc to 0.0
    if ((new->obj.rolling_ball.vel.x * old->obj.rolling_ball.vel.x) < 0.0)
    {

        new->obj.rolling_ball.vel.x = 0.0;
        new->obj.rolling_ball.acc.x = 0.0;
    }

    if ((new->obj.rolling_ball.vel.y * old->obj.rolling_ball.vel.y) < 0.0)
    {
        new->obj.rolling_ball.vel.y = 0.0;
        new->obj.rolling_ball.acc.y = 0.0;
    }
}

// function checking if rolling ball has stopped
unsigned char phylib_stopped(phylib_object *object)
{

    double speed = phylib_length(object->obj.rolling_ball.vel); // calculate speed of ball

    if (speed < PHYLIB_VEL_EPSILON) // if speed below threshold, convert to still ball
    {

        // setting all the members value
        unsigned char number = object->obj.rolling_ball.number;
        phylib_coord pos = object->obj.rolling_ball.pos;

        object->type = PHYLIB_STILL_BALL;
        object->obj.still_ball.number = number;
        object->obj.still_ball.pos = pos;

        return 1; // 1, ball has stopped
    }
    else
    {
        return 0; // 0, ball still moving
    }
}

// function calculating collision between ball and ball or ball and cushion
void phylib_bounce(phylib_object **a, phylib_object **b)
{

    if (*a == NULL || *b == NULL) // if either object null, return
    {
        return;
    }

    if ((*a)->type != PHYLIB_ROLLING_BALL) // if a isn;t rolling, return
    {
        return;
    }

    // variable declerations
    double v_rel_n, speedA, speedB, r_ab_length;
    unsigned char numOld;
    phylib_coord r_ab, v_rel, n, tempcoord;

    // check what ball a is colliding with
    switch ((*b)->type)
    {
    case PHYLIB_HCUSHION: // collding with horiztonal cushion

        // reverse the y vel and acc of a
        (*a)->obj.rolling_ball.vel.y = -(*a)->obj.rolling_ball.vel.y;
        (*a)->obj.rolling_ball.acc.y = -(*a)->obj.rolling_ball.acc.y;
        break;

    case PHYLIB_VCUSHION: // collding with horiztonal cushion

        // reverse the x vel and acc of a
        (*a)->obj.rolling_ball.vel.x = -(*a)->obj.rolling_ball.vel.x;
        (*a)->obj.rolling_ball.acc.x = -(*a)->obj.rolling_ball.acc.x;
        break;
    case PHYLIB_HOLE: // ball falls in hole, free the ball object
        // Free  memory allocated for  rolling ball and set pointer to NULL
        free(*a);
        *a = NULL;
        break;
    case PHYLIB_STILL_BALL: // ball collides with a still ball
    {

        // converting the still ball that was just hit to a rolling ball and proceeding without break to next case

        tempcoord = (*b)->obj.still_ball.pos;
        numOld = (*b)->obj.still_ball.number;
        (*b)->type = PHYLIB_ROLLING_BALL;
        (*b)->obj.rolling_ball.number = numOld;
        (*b)->obj.rolling_ball.pos = tempcoord;
        (*b)->obj.rolling_ball.vel.x = 0.0;
        (*b)->obj.rolling_ball.vel.y = 0.0;
        (*b)->obj.rolling_ball.acc.x = 0.0;
        (*b)->obj.rolling_ball.acc.y = 0.0;
        // No break here
    }
    case PHYLIB_ROLLING_BALL: // b is a rolling ball

        // relative pos and vel of the two balls
        r_ab = phylib_sub((*a)->obj.rolling_ball.pos, (*b)->obj.rolling_ball.pos);
        v_rel = phylib_sub((*a)->obj.rolling_ball.vel, (*b)->obj.rolling_ball.vel);

        // normailzing the vector and relative pos and vel of the two balls
        r_ab_length = phylib_length(r_ab);

        n.x = r_ab.x / r_ab_length;
        n.y = r_ab.y / r_ab_length;

        v_rel_n = phylib_dot_product(v_rel, n);

        // updating vel of the balls after the collision
        (*a)->obj.rolling_ball.vel.x -= v_rel_n * n.x;
        (*a)->obj.rolling_ball.vel.y -= v_rel_n * n.y;

        (*b)->obj.rolling_ball.vel.x += v_rel_n * n.x;
        (*b)->obj.rolling_ball.vel.y += v_rel_n * n.y;

        // updating speeds after the collision
        speedA = phylib_length((*a)->obj.rolling_ball.vel);
        speedB = phylib_length((*b)->obj.rolling_ball.vel);

        // updating the acceleration based on the drag coeffec
        if (speedA > PHYLIB_VEL_EPSILON)
        {
            (*a)->obj.rolling_ball.acc.x = -(*a)->obj.rolling_ball.vel.x / speedA * PHYLIB_DRAG;
            (*a)->obj.rolling_ball.acc.y = -(*a)->obj.rolling_ball.vel.y / speedA * PHYLIB_DRAG;
        }
        if (speedB > PHYLIB_VEL_EPSILON)
        {
            (*b)->obj.rolling_ball.acc.x = -(*b)->obj.rolling_ball.vel.x / speedB * PHYLIB_DRAG;
            (*b)->obj.rolling_ball.acc.y = -(*b)->obj.rolling_ball.vel.y / speedB * PHYLIB_DRAG;
        }

        break;

    default:
        printf("ERROR IN PHYLIB BOUNCE SWITCH CASE");
    }
}

// function to check number of rolling balls on a table
unsigned char phylib_rolling(phylib_table *t)
{

    unsigned char balls = 0;

    // Count the number of rolling balls on the table
    for (int i = 0; i < PHYLIB_MAX_OBJECTS; i++)
    {
        if (t->object[i] && t->object[i]->type == PHYLIB_ROLLING_BALL)
        {
            balls++; // increment balls for every rolling ball
        }
    }
    return balls;
}

// Function to simulate a segment of a pool (billiards) shot on a given table.
// It advances the simulation until a ball stops or a collision occurs, up to a maximum simulation time.
phylib_table *phylib_segment(phylib_table *table)
{
    int breakLoopFlag = 0; // Flag to break out of the loop once a significant event occurs (ball stops or collision).

    // Check if the input table is NULL or if there are no rolling balls on the table.
    // If either is true, the function returns NULL indicating no simulation was possible.
    if (table == NULL || phylib_rolling(table) == 0)
    {
        return NULL;
    }

    double time = PHYLIB_SIM_RATE; // Initialize simulation time step.

    // Create a copy of the table to simulate on, preventing alterations to the original table.
    phylib_table *tableCopy = phylib_copy_table(table);

    // Loop until the maximum simulation time is reached or a significant event occurs (breakloop flag is set).
    while (time < PHYLIB_MAX_TIME && !breakLoopFlag)
    {
        // Iterate over all possible objects on the table.
        for (int i = 0; i < PHYLIB_MAX_OBJECTS; i++)
        {
            // Check if the current object is a rolling ball.
            if (tableCopy->object[i] != NULL && (tableCopy->object)[i]->type == PHYLIB_ROLLING_BALL)
            {
                // Simulate the rolling motion of the current ball.
                phylib_roll(tableCopy->object[i], tableCopy->object[i], PHYLIB_SIM_RATE);

                // Check if the ball has stopped after the roll.
                if (phylib_stopped(tableCopy->object[i]))
                {
                    // Set flag to end simulation and break out of the loop.
                    breakLoopFlag = 1;
                    break;
                }

                // Check for collisions with other balls.
                for (int j = 0; j < PHYLIB_MAX_OBJECTS; j++)
                {
                    // Ensure we're not comparing the ball with itself and the other object is not NULL.
                    if ((tableCopy->object)[j] != NULL && j != i)
                    {
                        // Check if the distance between the two balls indicates a collision.
                        if (phylib_distance((tableCopy->object)[i], (tableCopy->object)[j]) < 0.0)
                        {
                            // Simulate the bounce effect due to the collision.
                            phylib_bounce(&((tableCopy->object)[i]), &((tableCopy->object)[j]));

                            // Set flag to end simulation and break out of the loop.
                            breakLoopFlag = 1;
                            break;
                        }
                    }
                }
            }
        }
        // Increment the simulation time by the simulation rate.
        time += PHYLIB_SIM_RATE;
    }

    // Update the total simulation time in the table copy before returning it.
    tableCopy->time += time;
    return tableCopy;
}






char *phylib_object_string(phylib_object *object)
{
    static char string[80];
    if (object == NULL)
    {
        snprintf(string, 80, "NULL;");
        return string;
    }
    switch (object->type)
    {
    case PHYLIB_STILL_BALL:
        snprintf(string, 80,
                 "STILL_BALL (%d,%6.1lf,%6.1lf)",
                 object->obj.still_ball.number,
                 object->obj.still_ball.pos.x,
                 object->obj.still_ball.pos.y);
        break;
    case PHYLIB_ROLLING_BALL:
        snprintf(string, 80,
                 "ROLLING_BALL (%d,%6.1lf,%6.1lf,%6.1lf,%6.1lf,%6.1lf,%6.1lf)",
                 object->obj.rolling_ball.number,
                 object->obj.rolling_ball.pos.x,
                 object->obj.rolling_ball.pos.y,
                 object->obj.rolling_ball.vel.x,
                 object->obj.rolling_ball.vel.y,
                 object->obj.rolling_ball.acc.x,
                 object->obj.rolling_ball.acc.y);
        break;
    case PHYLIB_HOLE:
        snprintf(string, 80,
                 "HOLE (%6.1lf,%6.1lf)",
                 object->obj.hole.pos.x,
                 object->obj.hole.pos.y);
        break;
    case PHYLIB_HCUSHION:
        snprintf(string, 80,
                 "HCUSHION (%6.1lf)",
                 object->obj.hcushion.y);
        break;
    case PHYLIB_VCUSHION:
        snprintf(string, 80,
                 "VCUSHION (%6.1lf)",
                 object->obj.vcushion.x);
        break;
    }
    return string;
}

// program wont run without main
int main()
{
}
