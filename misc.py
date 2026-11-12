help_options = {"/insert_class_periods": "This command allows the administrator to add valid periods, which defines valid data for commands relying on periods.",
                "/insert_class_names": "This command allows the administrator to add valid class names, which defines valid data for commands relying on class names.",
                "/insert_teacher_names": "This command allows the administrator to add valid teacher names, which defines valid data for commands relying on teacher names.",
                "/remove_periods": "This command allows the administrator to remove valid periods from current valid periods.",
                "/remove_class_names": "This command allows the administrator to remove class names from current valid class names.",
                "/remove_teacher_names": "This command allows the administrator to remove teacher names from current valid teacher names.",
                "/show_class_periods": "This command shows all valid periods in an embed.",
                "/show_class_names": "This command shows all valid classes in an embed.",
                "/show_teacher_names": "This command shows all valid teacher names in an embed.",
                "/show_homework": "This command shows all your entered (meaning using /add_homework) homeworks in an embed.",
                "/add_homework": "This command adds a homework to your to-do list (viewable via /show_homework). Must enter parameters such as class name, teacher, period, and due date. Valid data is shown using the show commands.",
                "/remove_homework": "This command removes a homework from your to-do list (viewable via /show_homework). Selects homework via the parameters in /show_homework.",
                "/change_homework_status": "This command changes the status of a homework from your to-do list (either completed or incomplete). Must enter parameters of said homework, found via /show_homework.",
                "/settings": "This command shows your current settings statuses.",
                "/change_settings": "This command changes your current settings statuses (click on a button to change).",
                "/show_schedule": "This command shows your current schedule. Schedule is used for auto-syncing. (Auto-syncing is when someone w/ the same schedule adds homework and it automatically adds to your to-do list.)",
                "/insert_into_schedule": "This command inserts one period of your day into the schedule (used for auto-syncing ref: show_schedule).",
                "/remove_from_schedule": "This command removes one period of your day from the schedule."
                }

option_description = {"/insert_class_periods": "Admin Command",
                      "/insert_class_names": "Admin Command",
                      "/insert_teacher_names": "Admin Command",
                      "/remove_periods": "Admin Command",
                      "/remove_class_names": "Admin Command",
                      "/remove_teacher_names": "Admin Command",
                      "/show_class_periods": "Display Command",
                      "/show_class_names": "Display Command",
                      "/show_teacher_names": "Display Command",
                      "/show_homework": "HW Command",
                      "/add_homework": "HW Command",
                      "/remove_homework": "HW Command",
                      "/change_homework_status": "HW Command",
                      "/settings": "Settings Command",
                      "/change_settings": "Settings Command",
                      "/show_schedule": "Sync Command",
                      "/insert_into_schedule": "Sync Command",
                      "/remove_from_schedule": "Sync Command"
                      }

feature_description = {"Auto-Sync": None,
                   "Auto-Delete": None,
                   "Homework Visibility": None,
                   "Auto-DM": None
}

feature_options = {"Auto-Sync": "When on, automatically updates your to-do list whenever someone with the same schedule adds a homework.",
                       "Auto-Delete": "When on, automatically deletes past homework from your to-do list.",
                       "Homework Visibility": "When on, makes all outputs from HomeworkBot ephemeral.",
                       "Auto-DM": "When on, automatically sends DMs when you have past due homework that is not complete."
}