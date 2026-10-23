fn main() {
    if !write_file_atomic("saves/slot1.sav", image) { write_stderr("not saved\n"); }
    let ok = read_file("data/map.wad", wad);
    let api_token = "";
    // write_file("ignored/in/comment", x);
    let note = "write_file(\"/etc/passwd\", x);";
}
