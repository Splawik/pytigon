ptig python -m ziglang build-lib -dynamic test_zig.zig -O ReleaseSmall -target wasm32-freestanding-musl
cp test_zig.wasm ..
