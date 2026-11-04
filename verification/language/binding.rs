// SPDX-FileCopyrightText: 2026 HeaviSolve contributors
// SPDX-License-Identifier: AGPL-3.0-or-later
#[allow(dead_code)]
mod slab {
    include!("slab.rs");
    pub fn run(refinement: usize) -> Vec<f64> {
        let (n, a, b) = assemble(refinement);
        solve(n, a, b)
    }
}
// Caller owns valid writable output/count; allocation failures may still abort.
// Status codes and synchronous buffer ownership match binding.cpp.
#[unsafe(no_mangle)]
pub unsafe extern "C" fn hs_slab(
    refinement: i32, output: *mut f64, capacity: usize, count: *mut usize,
) -> i32 {
    if count.is_null() { return 1; }
    unsafe { *count = 0; }
    if output.is_null() || !(1..=8).contains(&refinement) { return 1; }
    match std::panic::catch_unwind(|| slab::run(refinement as usize)) {
        Ok(values) => {
            unsafe { *count = values.len(); }
            if values.len() < 2 { return 3; }
            if capacity < values.len() { return 2; }
            unsafe { std::ptr::copy_nonoverlapping(values.as_ptr(), output, values.len()); }
            0
        }
        Err(_) => 3,
    }
}
