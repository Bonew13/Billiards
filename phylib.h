//Constants

#define PHYLIB_BALL_RADIUS (28.5) // mm
#define PHYLIB_BALL_DIAMETER (2*PHYLIB_BALL_RADIUS)
#define PHYLIB_HOLE_RADIUS (2*PHYLIB_BALL_DIAMETER)
#define PHYLIB_TABLE_LENGTH (2700.0) // mm
#define PHYLIB_TABLE_WIDTH (PHYLIB_TABLE_LENGTH/2.0) // mm
#define PHYLIB_SIM_RATE (0.0001) // s
#define PHYLIB_VEL_EPSILON (0.01) // mm/s
#define PHYLIB_DRAG (150.0) // mm/s^2
#define PHYLIB_MAX_TIME (600) // s
#define PHYLIB_MAX_OBJECTS (26)

//Polymorphic object types defined as enum. Enums are like grouped constants

typedef enum {
    PHYLIB_STILL_BALL = 0,
    PHYLIB_ROLLING_BALL = 1,
    PHYLIB_HOLE = 2,
    PHYLIB_HCUSHION = 3,
    PHYLIB_VCUSHION = 4,
} phylib_obj;

//Class representing a vector in 2 dimensions

typedef struct {
    double x;
    double y;
} phylib_coord;

//(Child) Classes representing objects on the table

//A ball that is not in motion and a position on the table
typedef struct {
    unsigned char number;
    phylib_coord pos;
} phylib_still_ball;

//A ball that is rolling, has a number (cue ball is 0), position on the table, velocity and negative acceleration due to friction
typedef struct{
    unsigned char number;
    phylib_coord pos;
    phylib_coord vel;
    phylib_coord acc;
}   phylib_rolling_ball;

//One of the 6 holes on the table. It has a position.
typedef struct{
    phylib_coord pos;
}   phylib_hole;

//Horizontal cushion (cushion along either of the two short sides of the table). Y-coordinate
typedef struct {
    double y;
} phylib_hcushion;

//Vertical cushion (cushion along either of the long short sides of the table). Y-coordinate
typedef struct {
    double x;
} phylib_vcushion;

//Polymorphic parent class of objects on the table

//C union that can store any of the above classes/structure in the same space
typedef union { //The union can only store one of these data types at a time.
    phylib_still_ball still_ball;
    phylib_rolling_ball rolling_ball;
    phylib_hole hole;
    phylib_hcushion hcushion;
    phylib_vcushion vcushion;
} phylib_untyped;

//Above union can store an object of any of the classes/structures, it cannot identify what the class of the object is. We need a structure for that.
typedef struct {
    phylib_obj type;
    phylib_untyped obj;
} phylib_object;

typedef struct {
    double time;
    phylib_object *object[PHYLIB_MAX_OBJECTS];
} phylib_table;

//Cunstructor Functions Prototypes

phylib_object *phylib_new_still_ball(unsigned char number, phylib_coord *pos);
phylib_object *phylib_new_rolling_ball(unsigned char number, phylib_coord *pos, phylib_coord *vel, phylib_coord *acc);
phylib_object *phylib_new_hole(phylib_coord *pos);
phylib_object *phylib_new_hcushion(double y);
phylib_object *phylib_new_vcushion(double x);
phylib_table *phylib_new_table(void);

//Utility Functions prototypes

void phylib_copy_object( phylib_object **dest, phylib_object **src );
phylib_table *phylib_copy_table( phylib_table *table );
void phylib_add_object( phylib_table *table, phylib_object *object );
void phylib_free_table( phylib_table *table );
phylib_coord phylib_sub( phylib_coord c1, phylib_coord c2 );
double phylib_length( phylib_coord c );
double phylib_dot_product( phylib_coord a, phylib_coord b );
double phylib_distance( phylib_object *obj1, phylib_object *obj2 );

//Simulation Function Prototypes
void phylib_roll( phylib_object *new, phylib_object *old, double time );
unsigned char phylib_stopped( phylib_object *object );
void phylib_bounce( phylib_object **a, phylib_object **b );
unsigned char phylib_rolling( phylib_table *t );
phylib_table *phylib_segment( phylib_table *table );
char *phylib_object_string(phylib_object *object);
