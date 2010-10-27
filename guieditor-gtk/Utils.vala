//From ValaIDE project.
namespace Utils {
    public static string? get_absolute_path (string? filename) {
        string absolute_path;
        absolute_path = filename;
        if (filename != null) {
          if (!Path.is_absolute (filename)) {
            absolute_path = Path.build_filename (Environment.get_current_dir (),
                                                 filename);
            if (!FileUtils.test (absolute_path, FileTest.EXISTS)) {
              absolute_path = filename;
              return null;
            }
          }
        }
        return absolute_path;
    }
}