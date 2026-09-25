/**
 * DUB.SAR 1.0 — Native Runtime Header (Stage 4).
 *
 * Implements:
 * - Exact rational arithmetic with __int128_t hardware acceleration and GCD reduction
 * - Canonical Mesopotamian sexagesimal formatting and parsing
 * - Structured determinations, properties, and retain logic
 * - First-class tablet data model (sequences, tables) and embedded standard archive
 * - Geometric primitives (right triangles, inclinations, feeds, turns, directions, rotations)
 * - Reference Discrete Fourier Transform and Cooley-Tukey Radix-2 Fast Fourier Transform
 */

#ifndef DUBSAR_RUNTIME_H
#define DUBSAR_RUNTIME_H

#include <stdint.h>
#include <stdbool.h>
#include <stddef.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>
#include <math.h>

#ifdef __cplusplus
extern "C" {
#endif

#if defined(__SIZEOF_INT128__)
typedef __int128_t dubsar_int128_t;
typedef __uint128_t dubsar_uint128_t;
#define DUBSAR_HAS_INT128 1
#else
#define DUBSAR_HAS_INT128 0
#endif

/* ==============================================================================
 * 1. Exact Arbitrary-Precision / 64-Bit Rational Type
 * ============================================================================== */

typedef struct {
    int64_t num;
    int64_t den;
} dubsar_rat_t;

int64_t dubsar_gcd(int64_t a, int64_t b);
dubsar_rat_t dubsar_rat_make(int64_t num, int64_t den);
dubsar_rat_t dubsar_rat_reduce(dubsar_rat_t r);

dubsar_rat_t dubsar_rat_add(dubsar_rat_t a, dubsar_rat_t b);
dubsar_rat_t dubsar_rat_sub(dubsar_rat_t a, dubsar_rat_t b);
dubsar_rat_t dubsar_rat_mul(dubsar_rat_t a, dubsar_rat_t b);
dubsar_rat_t dubsar_rat_div(dubsar_rat_t a, dubsar_rat_t b);
dubsar_rat_t dubsar_rat_mod(dubsar_rat_t a, dubsar_rat_t b);
dubsar_rat_t dubsar_rat_pow(dubsar_rat_t a, int64_t exp);
dubsar_rat_t dubsar_rat_neg(dubsar_rat_t a);
dubsar_rat_t dubsar_rat_abs(dubsar_rat_t a);

int64_t dubsar_rat_floor(dubsar_rat_t a);
int64_t dubsar_rat_ceil(dubsar_rat_t a);
int64_t dubsar_rat_nearest(dubsar_rat_t a);

int dubsar_rat_cmp(dubsar_rat_t a, dubsar_rat_t b);
int dubsar_rat_eq(dubsar_rat_t a, dubsar_rat_t b);
int dubsar_rat_ne(dubsar_rat_t a, dubsar_rat_t b);
int dubsar_rat_lt(dubsar_rat_t a, dubsar_rat_t b);
int dubsar_rat_le(dubsar_rat_t a, dubsar_rat_t b);
int dubsar_rat_gt(dubsar_rat_t a, dubsar_rat_t b);
int dubsar_rat_ge(dubsar_rat_t a, dubsar_rat_t b);

int dubsar_rat_is_regular(dubsar_rat_t a);
dubsar_rat_t dubsar_rat_square(dubsar_rat_t a);
int dubsar_rat_is_square(dubsar_rat_t a, dubsar_rat_t *out);
dubsar_rat_t dubsar_rat_sqrt_babylonian(dubsar_rat_t a, int iterations);

/* Formatting */
void dubsar_format_sexagesimal(dubsar_rat_t r, char *buf, size_t max_len);
void dubsar_format_canonical_rat(dubsar_rat_t r, char *buf, size_t max_len);

/* ==============================================================================
 * 2. Dimensioned Quantities
 * ============================================================================== */

typedef struct {
    dubsar_rat_t val;
    const char *unit; /* NULL or empty for dimensionless */
} dubsar_quant_t;

dubsar_quant_t dubsar_quant_make(dubsar_rat_t val, const char *unit);
void dubsar_quant_format(dubsar_quant_t q, char *buf, size_t max_len);

/* ==============================================================================
 * 3. Geometric Mathematics: Triangles, Inclinations, Turns, Directions
 * ============================================================================== */

typedef struct {
    dubsar_rat_t width;
    dubsar_rat_t length;
    dubsar_rat_t diagonal;
    int is_valid;
} dubsar_triangle_t;

dubsar_triangle_t dubsar_triangle_determine(dubsar_rat_t w, dubsar_rat_t l, dubsar_rat_t d,
                                            int has_w, int has_l, int has_d);
int dubsar_triangle_validate(dubsar_rat_t w, dubsar_rat_t l, dubsar_rat_t d);

typedef struct {
    dubsar_rat_t rise;
    dubsar_rat_t run;
    dubsar_rat_t inclination;
    dubsar_rat_t feed;
} dubsar_inclination_t;

dubsar_inclination_t dubsar_make_inclination(dubsar_rat_t rise, dubsar_rat_t run);

typedef struct {
    dubsar_rat_t fraction; /* fraction of a full turn in [0, 1) */
} dubsar_turn_t;

dubsar_turn_t dubsar_turn_make(int64_t num, int64_t den);
dubsar_turn_t dubsar_turn_add(dubsar_turn_t a, dubsar_turn_t b);
dubsar_turn_t dubsar_turn_sub(dubsar_turn_t a, dubsar_turn_t b);

typedef struct {
    dubsar_rat_t dx;
    dubsar_rat_t dy;
    dubsar_turn_t turn;
    int has_turn;
} dubsar_direction_t;

dubsar_direction_t dubsar_direction_from_run_rise(dubsar_rat_t run, dubsar_rat_t rise);
dubsar_direction_t dubsar_direction_from_turn(dubsar_turn_t t);

typedef struct {
    dubsar_rat_t magnitude;
    const char *unit;
    dubsar_direction_t direction;
} dubsar_directed_t;

dubsar_directed_t dubsar_directed_make(dubsar_rat_t mag, const char *unit, dubsar_direction_t dir);
dubsar_directed_t dubsar_directed_rotate(dubsar_directed_t q, dubsar_turn_t t);
dubsar_directed_t dubsar_directed_add(dubsar_directed_t a, dubsar_directed_t b);
dubsar_direction_t dubsar_direction_rotate(dubsar_direction_t d, dubsar_turn_t t);

/* ==============================================================================
 * 4. General Tagged Value System
 * ============================================================================== */

typedef struct dubsar_val dubsar_val_t;
typedef struct dubsar_tablet dubsar_tablet_t;

typedef enum {
    DUBSAR_VAL_EMPTY = 0,
    DUBSAR_VAL_RAT,
    DUBSAR_VAL_QUANT,
    DUBSAR_VAL_BOOL,
    DUBSAR_VAL_STR,
    DUBSAR_VAL_TRIANGLE,
    DUBSAR_VAL_INCLINATION,
    DUBSAR_VAL_TURN,
    DUBSAR_VAL_DIRECTION,
    DUBSAR_VAL_DIRECTED,
    DUBSAR_VAL_TABLET,
    DUBSAR_VAL_DETERMINATION
} dubsar_val_kind_t;

typedef struct {
    char name[64];
    dubsar_val_t *val;
} dubsar_field_t;

typedef struct {
    char name[64];
    size_t count;
    dubsar_field_t *fields;
} dubsar_determination_t;

struct dubsar_val {
    dubsar_val_kind_t kind;
    union {
        dubsar_rat_t rat;
        dubsar_quant_t quant;
        int boolean;
        const char *str;
        dubsar_triangle_t triangle;
        dubsar_inclination_t inclination;
        dubsar_turn_t turn;
        dubsar_direction_t direction;
        dubsar_directed_t directed;
        dubsar_tablet_t *tablet;
        dubsar_determination_t det;
    } as;
};

dubsar_val_t dubsar_val_empty(void);
dubsar_val_t dubsar_val_rat(dubsar_rat_t r);
dubsar_val_t dubsar_val_quant(dubsar_rat_t r, const char *unit);
dubsar_val_t dubsar_val_bool(int b);
dubsar_val_t dubsar_val_str(const char *s);
dubsar_val_t dubsar_val_triangle(dubsar_triangle_t t);
dubsar_val_t dubsar_val_inclination(dubsar_inclination_t inc);
dubsar_val_t dubsar_val_turn(dubsar_turn_t t);
dubsar_val_t dubsar_val_direction(dubsar_direction_t d);
dubsar_val_t dubsar_val_directed(dubsar_directed_t d);
dubsar_val_t dubsar_val_tablet(dubsar_tablet_t *t);

dubsar_val_t dubsar_val_get_field(dubsar_val_t val, const char *field);
void dubsar_format_val(dubsar_val_t val, char *buf, size_t max_len);
void dubsar_print_val(dubsar_val_t val);

dubsar_val_t dubsar_val_add(dubsar_val_t a, dubsar_val_t b);
dubsar_val_t dubsar_val_sub(dubsar_val_t a, dubsar_val_t b);
dubsar_val_t dubsar_val_mul(dubsar_val_t a, dubsar_val_t b);
dubsar_val_t dubsar_val_div(dubsar_val_t a, dubsar_val_t b);
dubsar_val_t dubsar_val_mod(dubsar_val_t a, dubsar_val_t b);
dubsar_val_t dubsar_val_pow(dubsar_val_t a, dubsar_val_t b);
dubsar_val_t dubsar_val_neg(dubsar_val_t a);
dubsar_val_t dubsar_val_abs(dubsar_val_t a);
dubsar_val_t dubsar_val_floor(dubsar_val_t a);
dubsar_val_t dubsar_val_ceil(dubsar_val_t a);
dubsar_val_t dubsar_val_nearest(dubsar_val_t a);
dubsar_val_t dubsar_val_cmp_op(dubsar_val_t a, dubsar_val_t b, const char *op);
int dubsar_val_is_truthy(dubsar_val_t v);
dubsar_val_t dubsar_val_make_determination(const char *name, size_t count, const char **field_names, dubsar_val_t **field_ptrs);
dubsar_val_t dubsar_val_clone(dubsar_val_t v);
dubsar_val_t dubsar_val_rotate(dubsar_val_t target, dubsar_turn_t t);
dubsar_rat_t dubsar_val_to_rat(dubsar_val_t v);

typedef struct {
    size_t count;
    dubsar_val_t values[8];
} dubsar_tuple_t;

static inline dubsar_tuple_t dubsar_tuple_empty(void) {
    dubsar_tuple_t t;
    t.count = 0;
    return t;
}

static inline dubsar_tuple_t dubsar_tuple_1(dubsar_val_t v) {
    dubsar_tuple_t t;
    t.count = 1;
    t.values[0] = v;
    return t;
}

static inline dubsar_tuple_t dubsar_tuple_2(dubsar_val_t v1, dubsar_val_t v2) {
    dubsar_tuple_t t;
    t.count = 2;
    t.values[0] = v1;
    t.values[1] = v2;
    return t;
}

static inline dubsar_tuple_t dubsar_tuple_make(size_t count, dubsar_val_t *vals) {
    dubsar_tuple_t t;
    t.count = count > 8 ? 8 : count;
    for (size_t i = 0; i < t.count; ++i) t.values[i] = vals[i];
    return t;
}

/* ==============================================================================
 * 5. First-Class Tablet Data Model & Embedded Archive
 * ============================================================================== */

typedef enum {
    DUBSAR_TABLET_SEQUENCE = 0,
    DUBSAR_TABLET_TABLE,
    DUBSAR_TABLET_STRUCTURED
} dubsar_tablet_shape_t;

typedef struct {
    dubsar_val_t key;
    dubsar_val_t val;
} dubsar_entry_t;

struct dubsar_tablet {
    char name[64];
    dubsar_tablet_shape_t shape;
    size_t count;
    size_t capacity;
    dubsar_entry_t *entries;
    int is_working;
};

dubsar_tablet_t* dubsar_tablet_create_sequence(const char *name, size_t prealloc_len);
dubsar_tablet_t* dubsar_tablet_create_table(const char *name);
void dubsar_tablet_free(dubsar_tablet_t *t);

void dubsar_tablet_append(dubsar_tablet_t *t, dubsar_val_t val);
void dubsar_tablet_put(dubsar_tablet_t *t, dubsar_val_t key, dubsar_val_t val);
dubsar_val_t dubsar_tablet_take(dubsar_tablet_t *t, dubsar_val_t key);
int64_t dubsar_tablet_length(dubsar_tablet_t *t);
dubsar_val_t dubsar_tablet_first(dubsar_tablet_t *t);
dubsar_val_t dubsar_tablet_last(dubsar_tablet_t *t);
dubsar_val_t dubsar_tablet_seek_nearest(dubsar_tablet_t *t, dubsar_val_t target);

/* Archival lookups */
dubsar_val_t dubsar_archive_take(const char *tablet_name, dubsar_val_t key);

/* ==============================================================================
 * 6. Harmonic Analysis: Discrete & Fast Fourier Transforms
 * ============================================================================== */

dubsar_tablet_t* dubsar_tablet_dft(dubsar_tablet_t *sig, int inverse);
dubsar_tablet_t* dubsar_tablet_fft(dubsar_tablet_t *sig, int inverse);

/* ==============================================================================
 * 7. Program Execution Environment & Input Driver
 * ============================================================================== */

typedef struct {
    const char *input_arg;
    int input_consumed;
} dubsar_env_t;

extern dubsar_env_t g_dubsar_env;

void dubsar_init_env(int argc, char **argv);
dubsar_rat_t dubsar_read_input_rat(const char *prompt);
dubsar_val_t dubsar_read_input_val(const char *prompt);

#ifdef __cplusplus
}
#endif

#endif /* DUBSAR_RUNTIME_H */
