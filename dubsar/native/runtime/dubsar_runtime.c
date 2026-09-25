/**
 * DUB.SAR 1.0 — Native Runtime Implementation (Stage 4).
 */

#include "dubsar_runtime.h"

dubsar_env_t g_dubsar_env = {NULL, 0};

/* ==============================================================================
 * 1. Exact Arbitrary-Precision / 64-Bit Rational Type
 * ============================================================================== */

int64_t dubsar_gcd(int64_t a, int64_t b) {
    if (a < 0) a = -a;
    if (b < 0) b = -b;
    while (b != 0) {
        int64_t temp = b;
        b = a % b;
        a = temp;
    }
    return a;
}

#if DUBSAR_HAS_INT128
static dubsar_int128_t dubsar_gcd_128(dubsar_int128_t a, dubsar_int128_t b) {
    if (a < 0) a = -a;
    if (b < 0) b = -b;
    while (b != 0) {
        dubsar_int128_t temp = b;
        b = a % b;
        a = temp;
    }
    return a;
}
#endif

dubsar_rat_t dubsar_rat_make(int64_t num, int64_t den) {
    dubsar_rat_t r = {num, den};
    return dubsar_rat_reduce(r);
}

dubsar_rat_t dubsar_rat_reduce(dubsar_rat_t r) {
    if (r.den == 0) {
        fprintf(stderr, "DUB.SAR Error: Division by zero\n");
        exit(1);
    }
    if (r.num == 0) {
        return (dubsar_rat_t){0, 1};
    }
    if (r.den < 0) {
        r.num = -r.num;
        r.den = -r.den;
    }
    int64_t g = dubsar_gcd(r.num, r.den);
    if (g > 1) {
        r.num /= g;
        r.den /= g;
    }
    return r;
}

dubsar_rat_t dubsar_rat_add(dubsar_rat_t a, dubsar_rat_t b) {
#if DUBSAR_HAS_INT128
    dubsar_int128_t num = (dubsar_int128_t)a.num * b.den + (dubsar_int128_t)b.num * a.den;
    dubsar_int128_t den = (dubsar_int128_t)a.den * b.den;
    dubsar_int128_t g = dubsar_gcd_128(num, den);
    num /= g;
    den /= g;
    if (den < 0) { num = -num; den = -den; }
    return (dubsar_rat_t){(int64_t)num, (int64_t)den};
#else
    int64_t g = dubsar_gcd(a.den, b.den);
    int64_t d1 = b.den / g;
    int64_t d2 = a.den / g;
    int64_t num = a.num * d1 + b.num * d2;
    int64_t g2 = dubsar_gcd(num, g);
    num /= g2;
    int64_t den = d2 * (b.den / g2);
    return (dubsar_rat_t){num, den};
#endif
}

dubsar_rat_t dubsar_rat_sub(dubsar_rat_t a, dubsar_rat_t b) {
#if DUBSAR_HAS_INT128
    dubsar_int128_t num = (dubsar_int128_t)a.num * b.den - (dubsar_int128_t)b.num * a.den;
    dubsar_int128_t den = (dubsar_int128_t)a.den * b.den;
    dubsar_int128_t g = dubsar_gcd_128(num, den);
    num /= g;
    den /= g;
    if (den < 0) { num = -num; den = -den; }
    return (dubsar_rat_t){(int64_t)num, (int64_t)den};
#else
    return dubsar_rat_add(a, (dubsar_rat_t){-b.num, b.den});
#endif
}

dubsar_rat_t dubsar_rat_mul(dubsar_rat_t a, dubsar_rat_t b) {
#if DUBSAR_HAS_INT128
    dubsar_int128_t num = (dubsar_int128_t)a.num * b.num;
    dubsar_int128_t den = (dubsar_int128_t)a.den * b.den;
    dubsar_int128_t g = dubsar_gcd_128(num, den);
    num /= g;
    den /= g;
    if (den < 0) { num = -num; den = -den; }
    return (dubsar_rat_t){(int64_t)num, (int64_t)den};
#else
    int64_t g1 = dubsar_gcd(a.num, b.den);
    int64_t g2 = dubsar_gcd(b.num, a.den);
    int64_t num = (a.num / g1) * (b.num / g2);
    int64_t den = (a.den / g2) * (b.den / g1);
    if (den < 0) { num = -num; den = -den; }
    return (dubsar_rat_t){num, den};
#endif
}

dubsar_rat_t dubsar_rat_div(dubsar_rat_t a, dubsar_rat_t b) {
    if (b.num == 0) {
        fprintf(stderr, "DUB.SAR Error: Division by zero\n");
        exit(1);
    }
    return dubsar_rat_mul(a, (dubsar_rat_t){b.den, b.num});
}

dubsar_rat_t dubsar_rat_mod(dubsar_rat_t a, dubsar_rat_t b) {
    if (b.num == 0) {
        fprintf(stderr, "DUB.SAR Error: Modulo by zero\n");
        exit(1);
    }
    dubsar_rat_t div_val = dubsar_rat_div(a, b);
    int64_t floor_val = dubsar_rat_floor(div_val);
    dubsar_rat_t sub_part = dubsar_rat_mul(b, (dubsar_rat_t){floor_val, 1});
    return dubsar_rat_sub(a, sub_part);
}

dubsar_rat_t dubsar_rat_pow(dubsar_rat_t a, int64_t exp) {
    if (exp == 0) return (dubsar_rat_t){1, 1};
    if (exp < 0) {
        if (a.num == 0) {
            fprintf(stderr, "DUB.SAR Error: Zero cannot be raised to negative power\n");
            exit(1);
        }
        return dubsar_rat_pow((dubsar_rat_t){a.den, a.num}, -exp);
    }
    dubsar_rat_t base = a;
    dubsar_rat_t result = {1, 1};
    while (exp > 0) {
        if (exp & 1) result = dubsar_rat_mul(result, base);
        base = dubsar_rat_mul(base, base);
        exp >>= 1;
    }
    return result;
}

dubsar_rat_t dubsar_rat_neg(dubsar_rat_t a) {
    return (dubsar_rat_t){-a.num, a.den};
}

dubsar_rat_t dubsar_rat_abs(dubsar_rat_t a) {
    return (dubsar_rat_t){a.num < 0 ? -a.num : a.num, a.den};
}

int64_t dubsar_rat_floor(dubsar_rat_t a) {
    int64_t q = a.num / a.den;
    int64_t r = a.num % a.den;
    if (a.num < 0 && r != 0) q--;
    return q;
}

int64_t dubsar_rat_ceil(dubsar_rat_t a) {
    int64_t q = a.num / a.den;
    int64_t r = a.num % a.den;
    if (a.num > 0 && r != 0) q++;
    return q;
}

int64_t dubsar_rat_nearest(dubsar_rat_t a) {
    int64_t num = a.num;
    int64_t den = a.den;
    if (num >= 0) {
        return (2 * num + den) / (2 * den);
    } else {
        int64_t abs_num = -num;
        int64_t abs_res = (2 * abs_num + den) / (2 * den);
        return -abs_res;
    }
}

int dubsar_rat_cmp(dubsar_rat_t a, dubsar_rat_t b) {
#if DUBSAR_HAS_INT128
    dubsar_int128_t diff = (dubsar_int128_t)a.num * b.den - (dubsar_int128_t)b.num * a.den;
    if (diff < 0) return -1;
    if (diff > 0) return 1;
    return 0;
#else
    dubsar_rat_t d = dubsar_rat_sub(a, b);
    if (d.num < 0) return -1;
    if (d.num > 0) return 1;
    return 0;
#endif
}

int dubsar_rat_eq(dubsar_rat_t a, dubsar_rat_t b) { return dubsar_rat_cmp(a, b) == 0; }
int dubsar_rat_ne(dubsar_rat_t a, dubsar_rat_t b) { return dubsar_rat_cmp(a, b) != 0; }
int dubsar_rat_lt(dubsar_rat_t a, dubsar_rat_t b) { return dubsar_rat_cmp(a, b) < 0; }
int dubsar_rat_le(dubsar_rat_t a, dubsar_rat_t b) { return dubsar_rat_cmp(a, b) <= 0; }
int dubsar_rat_gt(dubsar_rat_t a, dubsar_rat_t b) { return dubsar_rat_cmp(a, b) > 0; }
int dubsar_rat_ge(dubsar_rat_t a, dubsar_rat_t b) { return dubsar_rat_cmp(a, b) >= 0; }

int dubsar_rat_is_regular(dubsar_rat_t a) {
    int64_t d = a.den;
    while (d % 2 == 0) d /= 2;
    while (d % 3 == 0) d /= 3;
    while (d % 5 == 0) d /= 5;
    return (d == 1);
}

dubsar_rat_t dubsar_rat_square(dubsar_rat_t a) {
    return dubsar_rat_mul(a, a);
}

static int64_t isqrt64(int64_t n) {
    if (n <= 0) return 0;
    int64_t x0 = (int64_t)sqrt((double)n);
    while ((x0 + 1) * (x0 + 1) <= n) x0++;
    while (x0 * x0 > n) x0--;
    return x0;
}

int dubsar_rat_is_square(dubsar_rat_t a, dubsar_rat_t *out) {
    if (a.num < 0) return 0;
    if (a.num == 0) {
        if (out) *out = (dubsar_rat_t){0, 1};
        return 1;
    }
    int64_t sn = isqrt64(a.num);
    int64_t sd = isqrt64(a.den);
    if (sn * sn == a.num && sd * sd == a.den) {
        if (out) *out = (dubsar_rat_t){sn, sd};
        return 1;
    }
    return 0;
}

dubsar_rat_t dubsar_rat_sqrt_babylonian(dubsar_rat_t a, int iterations) {
    if (a.num < 0) {
        fprintf(stderr, "DUB.SAR Error: Negative quantity has no real square root\n");
        exit(1);
    }
    if (a.num == 0) return (dubsar_rat_t){0, 1};
    dubsar_rat_t exact;
    if (dubsar_rat_is_square(a, &exact)) return exact;

    int64_t sn = isqrt64(a.num);
    int64_t sd = isqrt64(a.den);
    if (sn == 0) sn = 1;
    if (sd == 0) sd = 1;
    dubsar_rat_t x = dubsar_rat_make(sn, sd);
    dubsar_rat_t half = {1, 2};

    for (int i = 0; i < iterations; ++i) {
        dubsar_rat_t div = dubsar_rat_div(a, x);
        dubsar_rat_t sum = dubsar_rat_add(x, div);
        x = dubsar_rat_mul(sum, half);
    }
    return x;
}

void dubsar_format_sexagesimal(dubsar_rat_t r, char *buf, size_t max_len) {
    if (r.den == 1) {
        snprintf(buf, max_len, "%lld", (long long)r.num);
        return;
    }
    const char *sign = r.num < 0 ? "-" : "";
    int64_t abs_num = r.num < 0 ? -r.num : r.num;
    int64_t whole = abs_num / r.den;
    int64_t rem = abs_num % r.den;

    char digits[256];
    digits[0] = '\0';
    int count = 0;
    int first = 1;
    while (rem > 0 && count < 10) {
        rem *= 60;
        int64_t digit = rem / r.den;
        rem %= r.den;
        char part[32];
        if (first) {
            snprintf(part, sizeof(part), "%lld", (long long)digit);
            first = 0;
        } else {
            snprintf(part, sizeof(part), ",%lld", (long long)digit);
        }
        strncat(digits, part, sizeof(digits) - strlen(digits) - 1);
        count++;
    }
    if (first) {
        strncpy(digits, "0", sizeof(digits) - 1);
    }
    snprintf(buf, max_len, "%s%lld;%s", sign, (long long)whole, digits);
}

void dubsar_format_canonical_rat(dubsar_rat_t r, char *buf, size_t max_len) {
    if (r.den == 1) {
        snprintf(buf, max_len, "%lld", (long long)r.num);
        return;
    }
    if (dubsar_rat_is_regular(r)) {
        dubsar_format_sexagesimal(r, buf, max_len);
        return;
    }
    int64_t abs_num = r.num < 0 ? -r.num : r.num;
    if (abs_num >= r.den) {
        int64_t whole = r.num / r.den;
        int64_t rem = abs_num % r.den;
        if (rem == 0) {
            snprintf(buf, max_len, "%lld", (long long)whole);
            return;
        }
        if (r.num < 0) {
            int64_t abs_w = whole < 0 ? -whole : whole;
            snprintf(buf, max_len, "-(%lld + %lld/%lld)", (long long)abs_w, (long long)rem, (long long)r.den);
        } else {
            snprintf(buf, max_len, "%lld + %lld/%lld", (long long)whole, (long long)rem, (long long)r.den);
        }
        return;
    }
    snprintf(buf, max_len, "%lld/%lld", (long long)r.num, (long long)r.den);
}

/* ==============================================================================
 * 2. Dimensioned Quantities
 * ============================================================================== */

dubsar_quant_t dubsar_quant_make(dubsar_rat_t val, const char *unit) {
    dubsar_quant_t q;
    q.val = val;
    q.unit = unit;
    return q;
}

void dubsar_quant_format(dubsar_quant_t q, char *buf, size_t max_len) {
    char rat_buf[128];
    dubsar_format_canonical_rat(q.val, rat_buf, sizeof(rat_buf));
    if (q.unit && q.unit[0] != '\0') {
        snprintf(buf, max_len, "%s %s", rat_buf, q.unit);
    } else {
        snprintf(buf, max_len, "%s", rat_buf);
    }
}

/* ==============================================================================
 * 3. Geometric Mathematics: Triangles, Inclinations, Turns, Directions
 * ============================================================================== */

dubsar_triangle_t dubsar_triangle_determine(dubsar_rat_t w, dubsar_rat_t l, dubsar_rat_t d,
                                            int has_w, int has_l, int has_d) {
    dubsar_triangle_t tri = {w, l, d, 0};
    if (has_w && has_l && !has_d) {
        // d = sqrt(w^2 + l^2)
        dubsar_rat_t sum = dubsar_rat_add(dubsar_rat_square(w), dubsar_rat_square(l));
        dubsar_rat_t diag;
        if (dubsar_rat_is_square(sum, &diag)) {
            tri.diagonal = diag;
            tri.is_valid = 1;
        } else {
            tri.diagonal = dubsar_rat_sqrt_babylonian(sum, 4);
            tri.is_valid = 0;
        }
    } else if (has_w && has_d && !has_l) {
        // l = sqrt(d^2 - w^2)
        dubsar_rat_t diff = dubsar_rat_sub(dubsar_rat_square(d), dubsar_rat_square(w));
        dubsar_rat_t len;
        if (dubsar_rat_is_square(diff, &len)) {
            tri.length = len;
            tri.is_valid = 1;
        } else {
            tri.length = dubsar_rat_sqrt_babylonian(diff, 4);
            tri.is_valid = 0;
        }
    } else if (has_l && has_d && !has_w) {
        // w = sqrt(d^2 - l^2)
        dubsar_rat_t diff = dubsar_rat_sub(dubsar_rat_square(d), dubsar_rat_square(l));
        dubsar_rat_t wid;
        if (dubsar_rat_is_square(diff, &wid)) {
            tri.width = wid;
            tri.is_valid = 1;
        } else {
            tri.width = dubsar_rat_sqrt_babylonian(diff, 4);
            tri.is_valid = 0;
        }
    } else if (has_w && has_l && has_d) {
        tri.is_valid = dubsar_triangle_validate(w, l, d);
    }
    return tri;
}

int dubsar_triangle_validate(dubsar_rat_t w, dubsar_rat_t l, dubsar_rat_t d) {
    dubsar_rat_t lhs = dubsar_rat_add(dubsar_rat_square(w), dubsar_rat_square(l));
    dubsar_rat_t rhs = dubsar_rat_square(d);
    return dubsar_rat_eq(lhs, rhs);
}

dubsar_inclination_t dubsar_make_inclination(dubsar_rat_t rise, dubsar_rat_t run) {
    dubsar_inclination_t inc;
    inc.rise = rise;
    inc.run = run;
    inc.inclination = dubsar_rat_div(rise, run);
    inc.feed = dubsar_rat_div(run, rise);
    return inc;
}

dubsar_turn_t dubsar_turn_make(int64_t num, int64_t den) {
    dubsar_rat_t r = dubsar_rat_make(num, den);
    // Wrap modulo 1: frac = r - floor(r)
    int64_t fl = dubsar_rat_floor(r);
    r = dubsar_rat_sub(r, (dubsar_rat_t){fl, 1});
    dubsar_turn_t t = {r};
    return t;
}

dubsar_turn_t dubsar_turn_add(dubsar_turn_t a, dubsar_turn_t b) {
    dubsar_rat_t sum = dubsar_rat_add(a.fraction, b.fraction);
    int64_t fl = dubsar_rat_floor(sum);
    return (dubsar_turn_t){dubsar_rat_sub(sum, (dubsar_rat_t){fl, 1})};
}

dubsar_turn_t dubsar_turn_sub(dubsar_turn_t a, dubsar_turn_t b) {
    dubsar_rat_t diff = dubsar_rat_sub(a.fraction, b.fraction);
    int64_t fl = dubsar_rat_floor(diff);
    return (dubsar_turn_t){dubsar_rat_sub(diff, (dubsar_rat_t){fl, 1})};
}

dubsar_direction_t dubsar_direction_from_run_rise(dubsar_rat_t run, dubsar_rat_t rise) {
    dubsar_direction_t dir;
    dir.dx = run;
    dir.dy = rise;
    dir.has_turn = 0;
    // Special exact cases
    if (rise.num == 0 && run.num > 0) {
        dir.turn = (dubsar_turn_t){{0, 1}};
        dir.has_turn = 1;
    } else if (run.num == 0 && rise.num > 0) {
        dir.turn = (dubsar_turn_t){{1, 4}};
        dir.has_turn = 1;
    } else if (rise.num == 0 && run.num < 0) {
        dir.turn = (dubsar_turn_t){{1, 2}};
        dir.has_turn = 1;
    } else if (run.num == 0 && rise.num < 0) {
        dir.turn = (dubsar_turn_t){{3, 4}};
        dir.has_turn = 1;
    } else if (dubsar_rat_eq(run, rise) && run.num > 0) {
        dir.turn = (dubsar_turn_t){{1, 8}};
        dir.has_turn = 1;
    }
    return dir;
}

dubsar_direction_t dubsar_direction_from_turn(dubsar_turn_t t) {
    dubsar_direction_t dir;
    dir.turn = t;
    dir.has_turn = 1;
    // Map canonical turns to exact orthogonal components
    dubsar_rat_t f = t.fraction;
    if (f.num == 0) {
        dir.dx = (dubsar_rat_t){1, 1};
        dir.dy = (dubsar_rat_t){0, 1};
    } else if (f.num == 1 && f.den == 4) {
        dir.dx = (dubsar_rat_t){0, 1};
        dir.dy = (dubsar_rat_t){1, 1};
    } else if (f.num == 1 && f.den == 2) {
        dir.dx = (dubsar_rat_t){-1, 1};
        dir.dy = (dubsar_rat_t){0, 1};
    } else if (f.num == 3 && f.den == 4) {
        dir.dx = (dubsar_rat_t){0, 1};
        dir.dy = (dubsar_rat_t){-1, 1};
    } else {
        // Approximate unit components using double
        double rad = 2.0 * 3.14159265358979323846 * ((double)f.num / (double)f.den);
        double c = cos(rad);
        double s = sin(rad);
        int64_t c_int = (int64_t)round(c * 1000000.0);
        int64_t s_int = (int64_t)round(s * 1000000.0);
        dir.dx = dubsar_rat_make(c_int, 1000000);
        dir.dy = dubsar_rat_make(s_int, 1000000);
    }
    return dir;
}

dubsar_directed_t dubsar_directed_make(dubsar_rat_t mag, const char *unit, dubsar_direction_t dir) {
    dubsar_directed_t d;
    d.magnitude = mag;
    d.unit = unit;
    d.direction = dir;
    return d;
}

dubsar_directed_t dubsar_directed_rotate(dubsar_directed_t q, dubsar_turn_t t) {
    dubsar_turn_t cur = q.direction.has_turn ? q.direction.turn : (dubsar_turn_t){{0, 1}};
    dubsar_turn_t next_turn = dubsar_turn_add(cur, t);
    dubsar_direction_t next_dir = dubsar_direction_from_turn(next_turn);
    return dubsar_directed_make(q.magnitude, q.unit, next_dir);
}

dubsar_direction_t dubsar_direction_rotate(dubsar_direction_t d, dubsar_turn_t t) {
    dubsar_turn_t cur = d.has_turn ? d.turn : (dubsar_turn_t){{0, 1}};
    dubsar_turn_t next_turn = dubsar_turn_add(cur, t);
    return dubsar_direction_from_turn(next_turn);
}

dubsar_directed_t dubsar_directed_add(dubsar_directed_t a, dubsar_directed_t b) {
    dubsar_direction_t da = a.direction.has_turn ? dubsar_direction_from_turn(a.direction.turn) : a.direction;
    dubsar_direction_t db = b.direction.has_turn ? dubsar_direction_from_turn(b.direction.turn) : b.direction;

    dubsar_rat_t x1 = dubsar_rat_mul(a.magnitude, da.dx);
    dubsar_rat_t y1 = dubsar_rat_mul(a.magnitude, da.dy);
    dubsar_rat_t x2 = dubsar_rat_mul(b.magnitude, db.dx);
    dubsar_rat_t y2 = dubsar_rat_mul(b.magnitude, db.dy);

    dubsar_rat_t x = dubsar_rat_add(x1, x2);
    dubsar_rat_t y = dubsar_rat_add(y1, y2);

    dubsar_rat_t mag_sq = dubsar_rat_add(dubsar_rat_square(x), dubsar_rat_square(y));
    dubsar_rat_t mag;
    if (!dubsar_rat_is_square(mag_sq, &mag)) {
        mag = dubsar_rat_sqrt_babylonian(mag_sq, 4);
    }
    dubsar_direction_t dir = dubsar_direction_from_run_rise(x, y);
    return dubsar_directed_make(mag, a.unit, dir);
}

/* ==============================================================================
 * 4. General Tagged Value System
 * ============================================================================== */

dubsar_val_t dubsar_val_empty(void) {
    dubsar_val_t v;
    v.kind = DUBSAR_VAL_EMPTY;
    return v;
}

dubsar_val_t dubsar_val_rat(dubsar_rat_t r) {
    dubsar_val_t v;
    v.kind = DUBSAR_VAL_RAT;
    v.as.rat = r;
    return v;
}

dubsar_val_t dubsar_val_quant(dubsar_rat_t r, const char *unit) {
    dubsar_val_t v;
    v.kind = DUBSAR_VAL_QUANT;
    v.as.quant = dubsar_quant_make(r, unit);
    return v;
}

dubsar_val_t dubsar_val_bool(int b) {
    dubsar_val_t v;
    v.kind = DUBSAR_VAL_BOOL;
    v.as.boolean = b ? 1 : 0;
    return v;
}

dubsar_val_t dubsar_val_str(const char *s) {
    dubsar_val_t v;
    v.kind = DUBSAR_VAL_STR;
    v.as.str = s;
    return v;
}

dubsar_val_t dubsar_val_triangle(dubsar_triangle_t t) {
    dubsar_val_t v;
    v.kind = DUBSAR_VAL_TRIANGLE;
    v.as.triangle = t;
    return v;
}

dubsar_val_t dubsar_val_inclination(dubsar_inclination_t inc) {
    dubsar_val_t v;
    v.kind = DUBSAR_VAL_INCLINATION;
    v.as.inclination = inc;
    return v;
}

dubsar_val_t dubsar_val_turn(dubsar_turn_t t) {
    dubsar_val_t v;
    v.kind = DUBSAR_VAL_TURN;
    v.as.turn = t;
    return v;
}

dubsar_val_t dubsar_val_direction(dubsar_direction_t d) {
    dubsar_val_t v;
    v.kind = DUBSAR_VAL_DIRECTION;
    v.as.direction = d;
    return v;
}

dubsar_val_t dubsar_val_directed(dubsar_directed_t d) {
    dubsar_val_t v;
    v.kind = DUBSAR_VAL_DIRECTED;
    v.as.directed = d;
    return v;
}

dubsar_val_t dubsar_val_tablet(dubsar_tablet_t *t) {
    dubsar_val_t v;
    v.kind = DUBSAR_VAL_TABLET;
    v.as.tablet = t;
    return v;
}

dubsar_rat_t dubsar_val_to_rat(dubsar_val_t v) {
    if (v.kind == DUBSAR_VAL_QUANT) return v.as.quant.val;
    if (v.kind == DUBSAR_VAL_RAT) return v.as.rat;
    return (dubsar_rat_t){0, 1};
}

dubsar_val_t dubsar_val_rotate(dubsar_val_t target, dubsar_turn_t t) {
    if (target.kind == DUBSAR_VAL_TURN) {
        return dubsar_val_turn(dubsar_turn_add(target.as.turn, t));
    }
    if (target.kind == DUBSAR_VAL_DIRECTION) {
        return dubsar_val_direction(dubsar_direction_rotate(target.as.direction, t));
    }
    if (target.kind == DUBSAR_VAL_DIRECTED) {
        return dubsar_val_directed(dubsar_directed_rotate(target.as.directed, t));
    }
    if (target.kind == DUBSAR_VAL_QUANT) {
        dubsar_direction_t base_dir = dubsar_direction_from_turn((dubsar_turn_t){{0, 1}});
        dubsar_directed_t dq = dubsar_directed_make(target.as.quant.val, target.as.quant.unit, base_dir);
        return dubsar_val_directed(dubsar_directed_rotate(dq, t));
    }
    if (target.kind == DUBSAR_VAL_RAT) {
        dubsar_direction_t base_dir = dubsar_direction_from_turn((dubsar_turn_t){{0, 1}});
        dubsar_directed_t dq = dubsar_directed_make(target.as.rat, NULL, base_dir);
        return dubsar_val_directed(dubsar_directed_rotate(dq, t));
    }
    return target;
}

dubsar_val_t dubsar_val_get_field(dubsar_val_t val, const char *field) {
    if (val.kind == DUBSAR_VAL_EMPTY) return dubsar_val_empty();
    if (val.kind == DUBSAR_VAL_TRIANGLE) {
        if (!strcmp(field, "width") || !strcmp(field, "short_side")) return dubsar_val_rat(val.as.triangle.width);
        if (!strcmp(field, "length") || !strcmp(field, "long_side")) return dubsar_val_rat(val.as.triangle.length);
        if (!strcmp(field, "diagonal") || !strcmp(field, "hypotenuse")) return dubsar_val_rat(val.as.triangle.diagonal);
        if (!strcmp(field, "is_valid") || !strcmp(field, "valid")) return dubsar_val_bool(val.as.triangle.is_valid);
        if (!strcmp(field, "inclination")) {
            dubsar_rat_t inc = dubsar_rat_div(val.as.triangle.length, val.as.triangle.width);
            return dubsar_val_rat(inc);
        }
        if (!strcmp(field, "feed")) {
            dubsar_rat_t fd = dubsar_rat_div(val.as.triangle.width, val.as.triangle.length);
            return dubsar_val_rat(fd);
        }
        if (!strcmp(field, "area")) {
            dubsar_rat_t pr = dubsar_rat_mul(val.as.triangle.width, val.as.triangle.length);
            return dubsar_val_rat(dubsar_rat_mul(pr, (dubsar_rat_t){1, 2}));
        }
    } else if (val.kind == DUBSAR_VAL_INCLINATION) {
        if (!strcmp(field, "rise")) return dubsar_val_rat(val.as.inclination.rise);
        if (!strcmp(field, "run")) return dubsar_val_rat(val.as.inclination.run);
        if (!strcmp(field, "inclination")) return dubsar_val_rat(val.as.inclination.inclination);
        if (!strcmp(field, "feed")) return dubsar_val_rat(val.as.inclination.feed);
    } else if (val.kind == DUBSAR_VAL_DIRECTED) {
        if (!strcmp(field, "magnitude")) return dubsar_val_quant(val.as.directed.magnitude, val.as.directed.unit);
        if (!strcmp(field, "direction")) return dubsar_val_direction(val.as.directed.direction);
    } else if (val.kind == DUBSAR_VAL_DIRECTION) {
        if (!strcmp(field, "turn")) return dubsar_val_turn(val.as.direction.turn);
        if (!strcmp(field, "dx") || !strcmp(field, "horizontal")) return dubsar_val_rat(val.as.direction.dx);
        if (!strcmp(field, "dy") || !strcmp(field, "vertical")) return dubsar_val_rat(val.as.direction.dy);
    } else if (val.kind == DUBSAR_VAL_DETERMINATION) {
        for (size_t i = 0; i < val.as.det.count; ++i) {
            if (!strcmp(val.as.det.fields[i].name, field)) {
                return *val.as.det.fields[i].val;
            }
        }
    }
    return dubsar_val_empty();
}

void dubsar_format_val(dubsar_val_t val, char *buf, size_t max_len) {
    switch (val.kind) {
        case DUBSAR_VAL_EMPTY:
            snprintf(buf, max_len, "empty");
            break;
        case DUBSAR_VAL_RAT:
            dubsar_format_canonical_rat(val.as.rat, buf, max_len);
            break;
        case DUBSAR_VAL_QUANT:
            dubsar_quant_format(val.as.quant, buf, max_len);
            break;
        case DUBSAR_VAL_BOOL:
            snprintf(buf, max_len, "%s", val.as.boolean ? "1" : "0");
            break;
        case DUBSAR_VAL_STR:
            snprintf(buf, max_len, "%s", val.as.str ? val.as.str : "");
            break;
        case DUBSAR_VAL_TRIANGLE: {
            char w_str[64], l_str[64], d_str[64];
            dubsar_format_canonical_rat(val.as.triangle.width, w_str, sizeof(w_str));
            dubsar_format_canonical_rat(val.as.triangle.length, l_str, sizeof(l_str));
            dubsar_format_canonical_rat(val.as.triangle.diagonal, d_str, sizeof(d_str));
            snprintf(buf, max_len, "right_triangle(width: %s, length: %s, diagonal: %s)", w_str, l_str, d_str);
            break;
        }
        case DUBSAR_VAL_INCLINATION: {
            char inc_str[64], fd_str[64];
            dubsar_format_canonical_rat(val.as.inclination.inclination, inc_str, sizeof(inc_str));
            dubsar_format_canonical_rat(val.as.inclination.feed, fd_str, sizeof(fd_str));
            snprintf(buf, max_len, "inclination(slope: %s, feed: %s)", inc_str, fd_str);
            break;
        }
        case DUBSAR_VAL_TURN: {
            char frac_str[64];
            dubsar_format_canonical_rat(val.as.turn.fraction, frac_str, sizeof(frac_str));
            if (val.as.turn.fraction.num == 1 && val.as.turn.fraction.den == 4) {
                snprintf(buf, max_len, "quarter-turn");
            } else if (val.as.turn.fraction.num == 1 && val.as.turn.fraction.den == 2) {
                snprintf(buf, max_len, "half-turn");
            } else {
                snprintf(buf, max_len, "%s-turn", frac_str);
            }
            break;
        }
        case DUBSAR_VAL_DIRECTION: {
            if (val.as.direction.has_turn) {
                char turn_buf[64];
                dubsar_val_t tv = dubsar_val_turn(val.as.direction.turn);
                dubsar_format_val(tv, turn_buf, sizeof(turn_buf));
                snprintf(buf, max_len, "direction(%s)", turn_buf);
            } else {
                char x_buf[64], y_buf[64];
                dubsar_format_canonical_rat(val.as.direction.dx, x_buf, sizeof(x_buf));
                dubsar_format_canonical_rat(val.as.direction.dy, y_buf, sizeof(y_buf));
                snprintf(buf, max_len, "direction(run: %s, rise: %s)", x_buf, y_buf);
            }
            break;
        }
        case DUBSAR_VAL_DIRECTED: {
            char mag_buf[64], dir_buf[128];
            dubsar_quant_t q = dubsar_quant_make(val.as.directed.magnitude, val.as.directed.unit);
            dubsar_quant_format(q, mag_buf, sizeof(mag_buf));
            dubsar_val_t dv = dubsar_val_direction(val.as.directed.direction);
            dubsar_format_val(dv, dir_buf, sizeof(dir_buf));
            snprintf(buf, max_len, "%s along %s", mag_buf, dir_buf);
            break;
        }
        case DUBSAR_VAL_TABLET: {
            snprintf(buf, max_len, "tablet \"%s\"", val.as.tablet ? val.as.tablet->name : "");
            break;
        }
        case DUBSAR_VAL_DETERMINATION: {
            snprintf(buf, max_len, "determination");
            break;
        }
    }
}

void dubsar_print_val(dubsar_val_t val) {
    if (val.kind == DUBSAR_VAL_DETERMINATION) {
        for (size_t i = 0; i < val.as.det.count; ++i) {
            dubsar_print_val(*val.as.det.fields[i].val);
        }
        return;
    }
    char buf[512];
    dubsar_format_val(val, buf, sizeof(buf));
    printf("%s\n", buf);
}

dubsar_val_t dubsar_val_add(dubsar_val_t a, dubsar_val_t b) {
    if (a.kind == DUBSAR_VAL_DIRECTED && b.kind == DUBSAR_VAL_DIRECTED) {
        return dubsar_val_directed(dubsar_directed_add(a.as.directed, b.as.directed));
    }
    const char *unit = (a.kind == DUBSAR_VAL_QUANT) ? a.as.quant.unit : ((b.kind == DUBSAR_VAL_QUANT) ? b.as.quant.unit : NULL);
    dubsar_rat_t ra = (a.kind == DUBSAR_VAL_QUANT) ? a.as.quant.val : a.as.rat;
    dubsar_rat_t rb = (b.kind == DUBSAR_VAL_QUANT) ? b.as.quant.val : b.as.rat;
    dubsar_rat_t res = dubsar_rat_add(ra, rb);
    return unit ? dubsar_val_quant(res, unit) : dubsar_val_rat(res);
}

dubsar_val_t dubsar_val_sub(dubsar_val_t a, dubsar_val_t b) {
    const char *unit = (a.kind == DUBSAR_VAL_QUANT) ? a.as.quant.unit : ((b.kind == DUBSAR_VAL_QUANT) ? b.as.quant.unit : NULL);
    dubsar_rat_t ra = (a.kind == DUBSAR_VAL_QUANT) ? a.as.quant.val : a.as.rat;
    dubsar_rat_t rb = (b.kind == DUBSAR_VAL_QUANT) ? b.as.quant.val : b.as.rat;
    dubsar_rat_t res = dubsar_rat_sub(ra, rb);
    return unit ? dubsar_val_quant(res, unit) : dubsar_val_rat(res);
}

dubsar_val_t dubsar_val_mul(dubsar_val_t a, dubsar_val_t b) {
    if (a.kind == DUBSAR_VAL_DIRECTED && (b.kind == DUBSAR_VAL_RAT || b.kind == DUBSAR_VAL_QUANT)) {
        dubsar_rat_t factor = (b.kind == DUBSAR_VAL_QUANT) ? b.as.quant.val : b.as.rat;
        dubsar_directed_t d = a.as.directed;
        d.magnitude = dubsar_rat_mul(d.magnitude, factor);
        return dubsar_val_directed(d);
    }
    const char *unit = (a.kind == DUBSAR_VAL_QUANT) ? a.as.quant.unit : ((b.kind == DUBSAR_VAL_QUANT) ? b.as.quant.unit : NULL);
    dubsar_rat_t ra = (a.kind == DUBSAR_VAL_QUANT) ? a.as.quant.val : a.as.rat;
    dubsar_rat_t rb = (b.kind == DUBSAR_VAL_QUANT) ? b.as.quant.val : b.as.rat;
    dubsar_rat_t res = dubsar_rat_mul(ra, rb);
    return unit ? dubsar_val_quant(res, unit) : dubsar_val_rat(res);
}

dubsar_val_t dubsar_val_div(dubsar_val_t a, dubsar_val_t b) {
    const char *unit = (a.kind == DUBSAR_VAL_QUANT && b.kind != DUBSAR_VAL_QUANT) ? a.as.quant.unit : NULL;
    dubsar_rat_t ra = (a.kind == DUBSAR_VAL_QUANT) ? a.as.quant.val : a.as.rat;
    dubsar_rat_t rb = (b.kind == DUBSAR_VAL_QUANT) ? b.as.quant.val : b.as.rat;
    dubsar_rat_t res = dubsar_rat_div(ra, rb);
    return unit ? dubsar_val_quant(res, unit) : dubsar_val_rat(res);
}

dubsar_val_t dubsar_val_mod(dubsar_val_t a, dubsar_val_t b) {
    const char *unit = (a.kind == DUBSAR_VAL_QUANT) ? a.as.quant.unit : NULL;
    dubsar_rat_t ra = (a.kind == DUBSAR_VAL_QUANT) ? a.as.quant.val : a.as.rat;
    dubsar_rat_t rb = (b.kind == DUBSAR_VAL_QUANT) ? b.as.quant.val : b.as.rat;
    dubsar_rat_t res = dubsar_rat_mod(ra, rb);
    return unit ? dubsar_val_quant(res, unit) : dubsar_val_rat(res);
}

dubsar_val_t dubsar_val_pow(dubsar_val_t a, dubsar_val_t b) {
    dubsar_rat_t ra = (a.kind == DUBSAR_VAL_QUANT) ? a.as.quant.val : a.as.rat;
    dubsar_rat_t rb = (b.kind == DUBSAR_VAL_QUANT) ? b.as.quant.val : b.as.rat;
    dubsar_rat_t res = dubsar_rat_pow(ra, rb.num);
    return dubsar_val_rat(res);
}

dubsar_val_t dubsar_val_neg(dubsar_val_t a) {
    if (a.kind == DUBSAR_VAL_QUANT) {
        return dubsar_val_quant(dubsar_rat_neg(a.as.quant.val), a.as.quant.unit);
    }
    return dubsar_val_rat(dubsar_rat_neg(a.as.rat));
}

dubsar_val_t dubsar_val_abs(dubsar_val_t a) {
    if (a.kind == DUBSAR_VAL_QUANT) {
        return dubsar_val_quant(dubsar_rat_abs(a.as.quant.val), a.as.quant.unit);
    }
    return dubsar_val_rat(dubsar_rat_abs(a.as.rat));
}

dubsar_val_t dubsar_val_floor(dubsar_val_t a) {
    dubsar_rat_t ra = (a.kind == DUBSAR_VAL_QUANT) ? a.as.quant.val : a.as.rat;
    int64_t fl = dubsar_rat_floor(ra);
    dubsar_rat_t res = {fl, 1};
    if (a.kind == DUBSAR_VAL_QUANT) return dubsar_val_quant(res, a.as.quant.unit);
    return dubsar_val_rat(res);
}

dubsar_val_t dubsar_val_ceil(dubsar_val_t a) {
    dubsar_rat_t ra = (a.kind == DUBSAR_VAL_QUANT) ? a.as.quant.val : a.as.rat;
    int64_t cl = dubsar_rat_ceil(ra);
    dubsar_rat_t res = {cl, 1};
    if (a.kind == DUBSAR_VAL_QUANT) return dubsar_val_quant(res, a.as.quant.unit);
    return dubsar_val_rat(res);
}

dubsar_val_t dubsar_val_nearest(dubsar_val_t a) {
    dubsar_rat_t ra = (a.kind == DUBSAR_VAL_QUANT) ? a.as.quant.val : a.as.rat;
    int64_t nr = dubsar_rat_nearest(ra);
    dubsar_rat_t res = {nr, 1};
    if (a.kind == DUBSAR_VAL_QUANT) return dubsar_val_quant(res, a.as.quant.unit);
    return dubsar_val_rat(res);
}

dubsar_val_t dubsar_val_cmp_op(dubsar_val_t a, dubsar_val_t b, const char *op) {
    int res = 0;
    if (a.kind == DUBSAR_VAL_EMPTY || b.kind == DUBSAR_VAL_EMPTY) {
        if (!strcmp(op, "<") || !strcmp(op, "lesser")) {
            res = (b.kind == DUBSAR_VAL_EMPTY && a.kind != DUBSAR_VAL_EMPTY);
        } else if (!strcmp(op, "<=")) {
            res = (b.kind == DUBSAR_VAL_EMPTY);
        } else if (!strcmp(op, ">") || !strcmp(op, "greater")) {
            res = (a.kind == DUBSAR_VAL_EMPTY && b.kind != DUBSAR_VAL_EMPTY);
        } else if (!strcmp(op, ">=")) {
            res = (a.kind == DUBSAR_VAL_EMPTY);
        } else if (!strcmp(op, "==")) {
            res = (a.kind == DUBSAR_VAL_EMPTY && b.kind == DUBSAR_VAL_EMPTY);
        } else if (!strcmp(op, "!=")) {
            res = !(a.kind == DUBSAR_VAL_EMPTY && b.kind == DUBSAR_VAL_EMPTY);
        }
        return dubsar_val_bool(res);
    }
    dubsar_rat_t ra = (a.kind == DUBSAR_VAL_QUANT) ? a.as.quant.val : a.as.rat;
    dubsar_rat_t rb = (b.kind == DUBSAR_VAL_QUANT) ? b.as.quant.val : b.as.rat;
    int cmp = dubsar_rat_cmp(ra, rb);
    if (!strcmp(op, "<") || !strcmp(op, "lesser")) res = cmp < 0;
    else if (!strcmp(op, "<=")) res = cmp <= 0;
    else if (!strcmp(op, ">") || !strcmp(op, "greater")) res = cmp > 0;
    else if (!strcmp(op, ">=")) res = cmp >= 0;
    else if (!strcmp(op, "==")) res = cmp == 0;
    else if (!strcmp(op, "!=")) res = cmp != 0;
    return dubsar_val_bool(res);
}

int dubsar_val_is_truthy(dubsar_val_t v) {
    if (v.kind == DUBSAR_VAL_EMPTY) return 0;
    if (v.kind == DUBSAR_VAL_BOOL) return v.as.boolean != 0;
    if (v.kind == DUBSAR_VAL_RAT) return v.as.rat.num != 0;
    if (v.kind == DUBSAR_VAL_QUANT) return v.as.quant.val.num != 0;
    return 1;
}

dubsar_val_t dubsar_val_make_determination(const char *name, size_t count, const char **field_names, dubsar_val_t **field_ptrs) {
    dubsar_val_t v;
    v.kind = DUBSAR_VAL_DETERMINATION;
    strncpy(v.as.det.name, name ? name : "determination", sizeof(v.as.det.name) - 1);
    v.as.det.name[sizeof(v.as.det.name) - 1] = '\0';
    v.as.det.count = count;
    v.as.det.fields = (dubsar_field_t*)malloc(sizeof(dubsar_field_t) * (count > 0 ? count : 1));
    for (size_t i = 0; i < count; ++i) {
        strncpy(v.as.det.fields[i].name, field_names[i], sizeof(v.as.det.fields[i].name) - 1);
        v.as.det.fields[i].name[sizeof(v.as.det.fields[i].name) - 1] = '\0';
        v.as.det.fields[i].val = field_ptrs[i];
    }
    return v;
}

dubsar_val_t dubsar_val_clone(dubsar_val_t v) {
    if (v.kind == DUBSAR_VAL_DETERMINATION) {
        dubsar_val_t copy = v;
        size_t count = v.as.det.count;
        copy.as.det.fields = (dubsar_field_t*)malloc(sizeof(dubsar_field_t) * (count > 0 ? count : 1));
        for (size_t i = 0; i < count; ++i) {
            strncpy(copy.as.det.fields[i].name, v.as.det.fields[i].name, sizeof(copy.as.det.fields[i].name) - 1);
            copy.as.det.fields[i].name[sizeof(copy.as.det.fields[i].name) - 1] = '\0';
            copy.as.det.fields[i].val = (dubsar_val_t*)malloc(sizeof(dubsar_val_t));
            *(copy.as.det.fields[i].val) = *(v.as.det.fields[i].val);
        }
        return copy;
    }
    return v;
}

/* ==============================================================================
 * 5. First-Class Tablet Data Model & Embedded Archive
 * ============================================================================== */

dubsar_tablet_t* dubsar_tablet_create_sequence(const char *name, size_t prealloc_len) {
    dubsar_tablet_t *t = (dubsar_tablet_t*)malloc(sizeof(dubsar_tablet_t));
    strncpy(t->name, name ? name : "sequence", sizeof(t->name) - 1);
    t->name[sizeof(t->name) - 1] = '\0';
    t->shape = DUBSAR_TABLET_SEQUENCE;
    t->count = 0;
    t->capacity = prealloc_len > 4 ? prealloc_len : 4;
    t->entries = (dubsar_entry_t*)malloc(sizeof(dubsar_entry_t) * t->capacity);
    t->is_working = 1;
    return t;
}

dubsar_tablet_t* dubsar_tablet_create_table(const char *name) {
    dubsar_tablet_t *t = (dubsar_tablet_t*)malloc(sizeof(dubsar_tablet_t));
    strncpy(t->name, name ? name : "table", sizeof(t->name) - 1);
    t->name[sizeof(t->name) - 1] = '\0';
    t->shape = DUBSAR_TABLET_TABLE;
    t->count = 0;
    t->capacity = 8;
    t->entries = (dubsar_entry_t*)malloc(sizeof(dubsar_entry_t) * t->capacity);
    t->is_working = 1;
    return t;
}

void dubsar_tablet_free(dubsar_tablet_t *t) {
    if (t) {
        if (t->entries) free(t->entries);
        free(t);
    }
}

void dubsar_tablet_append(dubsar_tablet_t *t, dubsar_val_t val) {
    if (t->count >= t->capacity) {
        t->capacity *= 2;
        t->entries = (dubsar_entry_t*)realloc(t->entries, sizeof(dubsar_entry_t) * t->capacity);
    }
    int64_t next_idx = (int64_t)t->count;
    t->entries[t->count].key = dubsar_val_rat(dubsar_rat_make(next_idx, 1));
    t->entries[t->count].val = val;
    t->count++;
}

void dubsar_tablet_put(dubsar_tablet_t *t, dubsar_val_t key, dubsar_val_t val) {
    for (size_t i = 0; i < t->count; ++i) {
        // Compare keys
        int match = 0;
        if (t->entries[i].key.kind == key.kind) {
            if (key.kind == DUBSAR_VAL_RAT) {
                match = dubsar_rat_eq(t->entries[i].key.as.rat, key.as.rat);
            } else if (key.kind == DUBSAR_VAL_STR && t->entries[i].key.as.str && key.as.str) {
                match = !strcmp(t->entries[i].key.as.str, key.as.str);
            }
        }
        if (match) {
            t->entries[i].val = val;
            return;
        }
    }
    if (t->count >= t->capacity) {
        t->capacity *= 2;
        t->entries = (dubsar_entry_t*)realloc(t->entries, sizeof(dubsar_entry_t) * t->capacity);
    }
    t->entries[t->count].key = key;
    t->entries[t->count].val = val;
    t->count++;
}

dubsar_val_t dubsar_tablet_take(dubsar_tablet_t *t, dubsar_val_t key) {
    for (size_t i = 0; i < t->count; ++i) {
        int match = 0;
        if (t->entries[i].key.kind == key.kind) {
            if (key.kind == DUBSAR_VAL_RAT) {
                match = dubsar_rat_eq(t->entries[i].key.as.rat, key.as.rat);
            } else if (key.kind == DUBSAR_VAL_STR && t->entries[i].key.as.str && key.as.str) {
                match = !strcmp(t->entries[i].key.as.str, key.as.str);
            }
        }
        if (match) {
            return t->entries[i].val;
        }
    }
    return dubsar_val_empty();
}

int64_t dubsar_tablet_length(dubsar_tablet_t *t) {
    return t ? (int64_t)t->count : 0;
}

dubsar_val_t dubsar_tablet_first(dubsar_tablet_t *t) {
    if (t && t->count > 0) return t->entries[0].val;
    return dubsar_val_empty();
}

dubsar_val_t dubsar_tablet_last(dubsar_tablet_t *t) {
    if (t && t->count > 0) return t->entries[t->count - 1].val;
    return dubsar_val_empty();
}

dubsar_val_t dubsar_tablet_seek_nearest(dubsar_tablet_t *t, dubsar_val_t target) {
    if (!t || t->count == 0) return dubsar_val_empty();
    if (target.kind != DUBSAR_VAL_RAT) return t->entries[0].val;

    dubsar_rat_t best_diff = {0, 0};
    dubsar_val_t best_val = dubsar_val_empty();
    int first = 1;

    for (size_t i = 0; i < t->count; ++i) {
        if (t->entries[i].key.kind == DUBSAR_VAL_RAT) {
            dubsar_rat_t diff = dubsar_rat_abs(dubsar_rat_sub(t->entries[i].key.as.rat, target.as.rat));
            if (first || dubsar_rat_lt(diff, best_diff)) {
                best_diff = diff;
                best_val = t->entries[i].val;
                first = 0;
            }
        }
    }
    return best_val;
}

/* Archival lookups for standard seeded reference tablets */
dubsar_val_t dubsar_archive_take(const char *tablet_name, dubsar_val_t key) {
    if (!strcmp(tablet_name, "powers-of-two")) {
        if (key.kind == DUBSAR_VAL_STR && key.as.str) {
            if (!strncmp(key.as.str, "len-", 4)) {
                int64_t target_len = atoll(key.as.str + 4);
                int exp = 0;
                while ((1LL << exp) < target_len && exp < 62) exp++;
                if ((1LL << exp) == target_len) {
                    return dubsar_val_rat(dubsar_rat_make(exp, 1));
                }
            } else if (!strncmp(key.as.str, "2^", 2)) {
                int exp = atoi(key.as.str + 2);
                return dubsar_val_rat(dubsar_rat_make(1LL << exp, 1));
            }
        } else if (key.kind == DUBSAR_VAL_RAT) {
            int64_t exp = key.as.rat.num;
            if (exp >= 0 && exp <= 30) {
                return dubsar_val_rat(dubsar_rat_make(1LL << exp, 1));
            }
        }
    } else if (!strcmp(tablet_name, "reciprocals")) {
        if (key.kind == DUBSAR_VAL_RAT && key.as.rat.den == 1) {
            int64_t n = key.as.rat.num;
            if (n > 0) {
                return dubsar_val_rat(dubsar_rat_make(1, n));
            }
        }
    } else if (!strcmp(tablet_name, "right-triangles")) {
        if (key.kind == DUBSAR_VAL_STR && key.as.str) {
            if (!strcmp(key.as.str, "3-4-5")) {
                return dubsar_val_triangle((dubsar_triangle_t){{3,1}, {4,1}, {5,1}, 1});
            } else if (!strcmp(key.as.str, "5-12-13")) {
                return dubsar_val_triangle((dubsar_triangle_t){{5,1}, {12,1}, {13,1}, 1});
            } else if (!strcmp(key.as.str, "8-15-17")) {
                return dubsar_val_triangle((dubsar_triangle_t){{8,1}, {15,1}, {17,1}, 1});
            } else if (!strcmp(key.as.str, "20-21-29")) {
                return dubsar_val_triangle((dubsar_triangle_t){{20,1}, {21,1}, {29,1}, 1});
            }
        }
    } else if (!strcmp(tablet_name, "inclinations")) {
        if (key.kind == DUBSAR_VAL_STR && key.as.str) {
            if (!strcmp(key.as.str, "gentle-ramp")) return dubsar_val_inclination(dubsar_make_inclination((dubsar_rat_t){1,1}, (dubsar_rat_t){5,1}));
            if (!strcmp(key.as.str, "standard-ramp")) return dubsar_val_inclination(dubsar_make_inclination((dubsar_rat_t){1,1}, (dubsar_rat_t){3,1}));
            if (!strcmp(key.as.str, "steep-ramp")) return dubsar_val_inclination(dubsar_make_inclination((dubsar_rat_t){1,1}, (dubsar_rat_t){2,1}));
            if (!strcmp(key.as.str, "diagonal-slope")) return dubsar_val_inclination(dubsar_make_inclination((dubsar_rat_t){1,1}, (dubsar_rat_t){1,1}));
            if (!strcmp(key.as.str, "wall-batter")) return dubsar_val_inclination(dubsar_make_inclination((dubsar_rat_t){6,1}, (dubsar_rat_t){1,1}));
        }
    }
    return dubsar_val_empty();
}

/* ==============================================================================
 * 6. Harmonic Analysis: Discrete & Fast Fourier Transforms
 * ============================================================================== */

dubsar_tablet_t* dubsar_tablet_dft(dubsar_tablet_t *sig, int inverse) {
    size_t N = sig ? sig->count : 0;
    dubsar_tablet_t *out = dubsar_tablet_create_sequence("dft", N);
    if (N == 0) return out;

    int sign = inverse ? 1 : -1;
    dubsar_rat_t norm = inverse ? (dubsar_rat_t){1, (int64_t)N} : (dubsar_rat_t){1, 1};

    for (size_t k = 0; k < N; ++k) {
        dubsar_directed_t acc = dubsar_directed_make((dubsar_rat_t){0, 1}, NULL, dubsar_direction_from_turn((dubsar_turn_t){{0, 1}}));
        for (size_t n = 0; n < N; ++n) {
            dubsar_val_t v = sig->entries[n].val;
            dubsar_directed_t sample;
            if (v.kind == DUBSAR_VAL_DIRECTED) {
                sample = v.as.directed;
            } else if (v.kind == DUBSAR_VAL_RAT) {
                sample = dubsar_directed_make(v.as.rat, NULL, dubsar_direction_from_turn((dubsar_turn_t){{0, 1}}));
            } else {
                sample = dubsar_directed_make((dubsar_rat_t){0, 1}, NULL, dubsar_direction_from_turn((dubsar_turn_t){{0, 1}}));
            }
            int64_t turn_num = (int64_t)k * (int64_t)n * sign;
            dubsar_turn_t rot = dubsar_turn_make(turn_num, (int64_t)N);
            dubsar_directed_t rotated = dubsar_directed_rotate(sample, rot);
            acc = dubsar_directed_add(acc, rotated);
        }
        acc.magnitude = dubsar_rat_mul(acc.magnitude, norm);
        dubsar_tablet_append(out, dubsar_val_directed(acc));
    }
    return out;
}

static dubsar_tablet_t* fft_recursive_internal(dubsar_tablet_t *sig, int inverse) {
    size_t N = sig->count;
    if (N <= 1) {
        dubsar_tablet_t *res = dubsar_tablet_create_sequence("fft_leaf", N);
        if (N == 1) dubsar_tablet_append(res, sig->entries[0].val);
        return res;
    }
    dubsar_tablet_t *even = dubsar_tablet_create_sequence("even", N / 2);
    dubsar_tablet_t *odd = dubsar_tablet_create_sequence("odd", N / 2);
    for (size_t i = 0; i < N; i += 2) {
        dubsar_tablet_append(even, sig->entries[i].val);
        dubsar_tablet_append(odd, sig->entries[i + 1].val);
    }
    dubsar_tablet_t *fft_even = fft_recursive_internal(even, inverse);
    dubsar_tablet_t *fft_odd = fft_recursive_internal(odd, inverse);
    dubsar_tablet_free(even);
    dubsar_tablet_free(odd);

    dubsar_tablet_t *out = dubsar_tablet_create_sequence("fft_merge", N);
    for (size_t i = 0; i < N; ++i) {
        dubsar_tablet_append(out, dubsar_val_empty());
    }

    int sign = inverse ? 1 : -1;
    for (size_t k = 0; k < N / 2; ++k) {
        dubsar_val_t ev_val = fft_even->entries[k].val;
        dubsar_val_t od_val = fft_odd->entries[k].val;
        dubsar_directed_t ev_dir = (ev_val.kind == DUBSAR_VAL_DIRECTED) ? ev_val.as.directed : dubsar_directed_make(ev_val.as.rat, NULL, dubsar_direction_from_turn((dubsar_turn_t){{0, 1}}));
        dubsar_directed_t od_dir = (od_val.kind == DUBSAR_VAL_DIRECTED) ? od_val.as.directed : dubsar_directed_make(od_val.as.rat, NULL, dubsar_direction_from_turn((dubsar_turn_t){{0, 1}}));

        dubsar_turn_t twiddle = dubsar_turn_make((int64_t)k * sign, (int64_t)N);
        dubsar_directed_t twiddled_odd = dubsar_directed_rotate(od_dir, twiddle);

        // out[k] = ev + twiddled_odd
        dubsar_directed_t p1 = dubsar_directed_add(ev_dir, twiddled_odd);
        // out[k + N/2] = ev - twiddled_odd = ev + rotate(twiddled_odd, half-turn)
        dubsar_directed_t neg_twiddled = dubsar_directed_rotate(twiddled_odd, dubsar_turn_make(1, 2));
        dubsar_directed_t p2 = dubsar_directed_add(ev_dir, neg_twiddled);

        out->entries[k].val = dubsar_val_directed(p1);
        out->entries[k + N / 2].val = dubsar_val_directed(p2);
    }
    dubsar_tablet_free(fft_even);
    dubsar_tablet_free(fft_odd);
    return out;
}

dubsar_tablet_t* dubsar_tablet_fft(dubsar_tablet_t *sig, int inverse) {
    size_t N = sig ? sig->count : 0;
    if (N == 0) return dubsar_tablet_create_sequence("fft", 0);
    // Check power of 2
    if ((N & (N - 1)) != 0) {
        // Fallback to reference DFT
        return dubsar_tablet_dft(sig, inverse);
    }
    dubsar_tablet_t *out = fft_recursive_internal(sig, inverse);
    if (inverse) {
        dubsar_rat_t norm = {1, (int64_t)N};
        for (size_t i = 0; i < N; ++i) {
            if (out->entries[i].val.kind == DUBSAR_VAL_DIRECTED) {
                out->entries[i].val.as.directed.magnitude = dubsar_rat_mul(out->entries[i].val.as.directed.magnitude, norm);
            }
        }
    }
    return out;
}

/* ==============================================================================
 * 7. Program Execution Environment & Input Driver
 * ============================================================================== */

void dubsar_init_env(int argc, char **argv) {
    for (int i = 1; i < argc; ++i) {
        if (!strncmp(argv[i], "--input=", 8)) {
            g_dubsar_env.input_arg = argv[i] + 8;
        } else if (!strcmp(argv[i], "--input") && i + 1 < argc) {
            g_dubsar_env.input_arg = argv[++i];
        }
    }
}

static dubsar_rat_t parse_number_str(const char *s) {
    while (*s == ' ') s++;
    int sign = 1;
    if (*s == '-') { sign = -1; s++; }
    else if (*s == '+') { s++; }

    // Check for sexagesimal ';'
    const char *semi = strchr(s, ';');
    if (semi) {
        int64_t whole = atoll(s);
        dubsar_rat_t res = {whole, 1};
        const char *p = semi + 1;
        int64_t place_den = 60;
        while (*p) {
            while (*p == ' ' || *p == ',') p++;
            if (!*p) break;
            int64_t digit = atoll(p);
            dubsar_rat_t part = dubsar_rat_make(digit, place_den);
            res = dubsar_rat_add(res, part);
            place_den *= 60;
            while (*p && *p != ',') p++;
        }
        res.num *= sign;
        return dubsar_rat_reduce(res);
    }

    // Check for decimal dot '.'
    const char *dot = strchr(s, '.');
    if (dot) {
        char buf[64];
        size_t idx = 0;
        int64_t decimals = 0;
        int after_dot = 0;
        for (const char *p = s; *p && idx < sizeof(buf) - 1; p++) {
            if (*p == '.') {
                after_dot = 1;
            } else if (*p >= '0' && *p <= '9') {
                buf[idx++] = *p;
                if (after_dot) decimals++;
            }
        }
        buf[idx] = '\0';
        int64_t num = atoll(buf);
        int64_t den = 1;
        for (int64_t i = 0; i < decimals; ++i) den *= 10;
        dubsar_rat_t res = dubsar_rat_make(num * sign, den);
        return res;
    }

    // Check for fraction '/'
    const char *slash = strchr(s, '/');
    if (slash) {
        int64_t num = atoll(s);
        int64_t den = atoll(slash + 1);
        return dubsar_rat_make(num * sign, den);
    }

    int64_t num = atoll(s);
    return (dubsar_rat_t){num * sign, 1};
}

dubsar_rat_t dubsar_read_input_rat(const char *prompt) {
    if (g_dubsar_env.input_arg && !g_dubsar_env.input_consumed) {
        g_dubsar_env.input_consumed = 1;
        return parse_number_str(g_dubsar_env.input_arg);
    }
    if (prompt && prompt[0]) {
        printf("%s: ", prompt);
        fflush(stdout);
    }
    char line[256];
    if (fgets(line, sizeof(line), stdin)) {
        size_t len = strlen(line);
        if (len > 0 && line[len - 1] == '\n') line[len - 1] = '\0';
        return parse_number_str(line);
    }
    return (dubsar_rat_t){0, 1};
}

dubsar_val_t dubsar_read_input_val(const char *prompt) {
    char line_buf[256];
    line_buf[0] = '\0';
    if (g_dubsar_env.input_arg && !g_dubsar_env.input_consumed) {
        g_dubsar_env.input_consumed = 1;
        strncpy(line_buf, g_dubsar_env.input_arg, sizeof(line_buf) - 1);
        line_buf[sizeof(line_buf) - 1] = '\0';
    } else {
        if (prompt && prompt[0]) {
            printf("%s: ", prompt);
            fflush(stdout);
        }
        if (fgets(line_buf, sizeof(line_buf), stdin)) {
            size_t len = strlen(line_buf);
            if (len > 0 && line_buf[len - 1] == '\n') line_buf[len - 1] = '\0';
        }
    }

    char *s = line_buf;
    while (*s == ' ') s++;
    if (!*s) return dubsar_val_empty();

    char num_part[128];
    char unit_part[128];
    num_part[0] = '\0';
    unit_part[0] = '\0';

    char *space = strchr(s, ' ');
    if (space) {
        size_t n_len = (size_t)(space - s);
        if (n_len >= sizeof(num_part)) n_len = sizeof(num_part) - 1;
        strncpy(num_part, s, n_len);
        num_part[n_len] = '\0';
        char *u = space + 1;
        while (*u == ' ') u++;
        strncpy(unit_part, u, sizeof(unit_part) - 1);
        unit_part[sizeof(unit_part) - 1] = '\0';
    } else {
        strncpy(num_part, s, sizeof(num_part) - 1);
        num_part[sizeof(num_part) - 1] = '\0';
    }

    dubsar_rat_t rat = parse_number_str(num_part);
    const char *unit = NULL;
    if (unit_part[0]) {
        unit = strdup(unit_part);
    } else if (prompt) {
        char p_lower[256];
        size_t plen = strlen(prompt);
        if (plen >= sizeof(p_lower)) plen = sizeof(p_lower) - 1;
        for (size_t i = 0; i < plen; ++i) {
            p_lower[i] = (char)tolower((unsigned char)prompt[i]);
        }
        p_lower[plen] = '\0';

        if (strstr(p_lower, "in days") || strstr(p_lower, "in day") || strstr(prompt, "in 𒌓")) {
            unit = "day";
        } else if (strstr(p_lower, "in hours") || strstr(p_lower, "in hour")) {
            unit = "hour";
        } else if (strstr(p_lower, "in minutes") || strstr(p_lower, "in minute")) {
            unit = "minute";
        } else if (strstr(p_lower, "in seconds") || strstr(p_lower, "in second")) {
            unit = "second";
        } else if (strstr(p_lower, "in months") || strstr(p_lower, "in month") || strstr(prompt, "in 𒌗")) {
            unit = "month";
        } else if (strstr(p_lower, "in years") || strstr(p_lower, "in year") || strstr(prompt, "in 𒈬")) {
            unit = "year";
        }
    }

    if (unit) {
        return dubsar_val_quant(rat, unit);
    }
    return dubsar_val_rat(rat);
}
