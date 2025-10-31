methods_map = {
    "AlertsService": {
        "ru_name": "Сервис уведомлений",
        "methods": {
            "handle_go_to_video_drafts": "Перейти к черновикам видео",
            "handle_go_to_main_menu": "Перейти в главное меню"
        }
    },
    "CreateCategoryService": {
        "ru_name": "Сервис создания категории",
        "methods": {
            "handle_user_message": "Обработать сообщение пользователя",
            "handle_confirm_cancel": "Подтвердить отмену",
            "handle_go_to_main_menu": "Перейти в главное меню"
        }
    },
    "UpdateCategoryService": {
        "ru_name": "Сервис обновления категории",
        "methods": {
            "handle_user_message": "Обработать сообщение пользователя",
            "handle_select_category": "Выбрать категорию",
            "handle_confirm_cancel": "Подтвердить отмену",
            "handle_go_to_main_menu": "Перейти в главное меню"
        }
    },
    "CreateOrganizationService": {
        "ru_name": "Сервис создания организации",
        "methods": {
            "handle_user_message": "Обработать сообщение пользователя",
            "handle_confirm_cancel": "Подтвердить отмену",
            "go_to_create_category": "Перейти к созданию категории",
            "handle_go_to_main_menu": "Перейти в главное меню"
        }
    },
    "UpdateOrganizationService": {
        "ru_name": "Сервис обновления организации",
        "methods": {
            "handle_user_message": "Обработать сообщение пользователя",
            "handle_confirm_cancel": "Подтвердить отмену",
            "handle_go_to_main_menu": "Перейти в главное меню"
        }
    },
    "ContentMenuService": {
        "ru_name": "Сервис меню контента",
        "methods": {
            "handle_go_to_publication_generation": "Перейти к генерации публикации",
            "handle_go_to_video_cut_generation": "Перейти к генерации видео нарезки",
            "handle_go_to_publication_drafts": "Перейти к черновикам публикаций",
            "handle_go_to_video_drafts": "Перейти к черновикам видео",
            "handle_go_to_publication_moderation": "Перейти к модерации публикаций",
            "handle_go_to_video_moderation": "Перейти к модерации видео",
            "handle_go_to_main_menu": "Перейти в главное меню",
            "handle_go_to_content_menu": "Перейти в меню контента"
        }
    },
    "GeneratePublicationService": {
        "ru_name": "Сервис генерации публикаций",
        "methods": {
            "handle_select_category": "Выбрать категорию",
            "handle_go_to_content_menu": "Перейти в меню контента",
            "handle_generate_text_prompt_input": "Ввести промпт для генерации текста",
            "handle_generate_publication_text_with_image": "Сгенерировать текст публикации с изображением",
            "handle_generate_publication_text": "Сгенерировать текст публикации",
            "go_to_create_category": "Перейти к созданию категории",
            "handle_regenerate_text": "Перегенерировать текст",
            "handle_regenerate_text_prompt_input": "Ввести промпт для перегенерации текста",
            "handle_edit_publication_text": "Редактировать текст публикации",
            "handle_edit_image_prompt_input": "Ввести промпт для редактирования изображения",
            "handle_image_upload": "Загрузить изображение",
            "handle_remove_image": "Удалить изображение",
            "handle_prev_image": "Предыдущее изображение",
            "handle_next_image": "Следующее изображение",
            "handle_add_to_drafts": "Добавить в черновики",
            "handle_send_to_moderation": "Отправить на модерацию",
            "handle_publish_now": "Опубликовать сейчас",
            "handle_toggle_social_network": "Переключить социальную сеть",
            "handle_compress_text": "Сжать текст",
            "handle_remove_photo_from_long_text": "Удалить фото из длинного текста",
            "handle_combine_images_start": "Начать объединение изображений",
            "handle_combine_with_current_image": "Объединить с текущим изображением",
            "handle_combine_image_from_scratch": "Объединить изображение с нуля",
            "handle_combine_image_upload": "Загрузить изображение для объединения",
            "handle_prev_combine_image": "Предыдущее объединяемое изображение",
            "handle_next_combine_image": "Следующее объединяемое изображение",
            "handle_delete_combine_image": "Удалить объединяемое изображение",
            "handle_back_from_combine_image_upload": "Вернуться из загрузки объединяемого изображения",
            "handle_combine_image_prompt_input": "Ввести промпт для объединения изображений",
            "handle_skip_combine_image_prompt": "Пропустить промпт для объединения изображений",
            "handle_edit_image_prompt_input_from_confirm_new_image": "Ввести промпт для редактирования из подтверждения нового изображения",
            "handle_combine_image_from_new_image": "Объединить изображение из нового изображения",
            "handle_confirm_new_image": "Подтвердить новое изображение",
            "handle_show_old_image": "Показать старое изображение",
            "handle_show_new_image": "Показать новое изображение",
            "handle_reject_new_image": "Отклонить новое изображение",
            "handle_auto_generate_image": "Автогенерация изображения",
            "handle_reference_generation_image_prompt_input": "Ввести промпт для генерации по референсу",
            "handle_reference_generation_image_upload": "Загрузить референсное изображение",
            "handle_back_from_custom_generation": "Вернуться из кастомной генерации",
            "handle_remove_reference_generation_image": "Удалить референсное изображение",
            "handle_use_current_image_as_reference": "Использовать текущее изображение как референс"
        }
    },
    "DraftPublicationService": {
        "ru_name": "Сервис черновиков публикаций",
        "methods": {
            "handle_navigate_publication": "Навигация по публикации",
            "handle_toggle_social_network": "Переключить социальную сеть",
            "handle_prev_image": "Предыдущее изображение",
            "handle_next_image": "Следующее изображение",
            "handle_send_to_moderation": "Отправить на модерацию",
            "handle_publish_now": "Опубликовать сейчас",
            "handle_regenerate_text": "Перегенерировать текст",
            "handle_regenerate_text_prompt_input": "Ввести промпт для перегенерации текста",
            "handle_edit_publication_text": "Редактировать текст публикации",
            "handle_generate_new_image": "Сгенерировать новое изображение",
            "handle_edit_image_prompt_input": "Ввести промпт для редактирования изображения",
            "handle_image_upload": "Загрузить изображение",
            "handle_remove_image": "Удалить изображение",
            "handle_save_edits": "Сохранить изменения",
            "handle_back_to_draft_list": "Вернуться к списку черновиков",
            "handle_compress_text": "Сжать текст",
            "handle_remove_photo_from_long_text": "Удалить фото из длинного текста",
            "handle_restore_previous_state": "Восстановить предыдущее состояние",
            "handle_back_to_content_menu": "Вернуться в меню контента",
            "handle_combine_images_start": "Начать объединение изображений",
            "handle_combine_with_current_image": "Объединить с текущим изображением",
            "handle_combine_image_from_scratch": "Объединить изображение с нуля",
            "handle_combine_image_upload": "Загрузить изображение для объединения",
            "handle_prev_combine_image": "Предыдущее объединяемое изображение",
            "handle_next_combine_image": "Следующее объединяемое изображение",
            "handle_back_from_combine_image_upload": "Вернуться из загрузки объединяемого изображения",
            "handle_delete_combine_image": "Удалить объединяемое изображение",
            "handle_combine_image_prompt_input": "Ввести промпт для объединения изображений",
            "handle_skip_combine_image_prompt": "Пропустить промпт для объединения изображений",
            "handle_combine_image_from_new_image": "Объединить изображение из нового изображения",
            "handle_edit_image_prompt_input_from_confirm_new_image": "Ввести промпт для редактирования из подтверждения нового изображения",
            "handle_confirm_new_image": "Подтвердить новое изображение",
            "handle_show_old_image": "Показать старое изображение",
            "handle_show_new_image": "Показать новое изображение",
            "handle_reject_new_image": "Отклонить новое изображение",
            "handle_auto_generate_image": "Автогенерация изображения",
            "handle_reference_generation_image_prompt_input": "Ввести промпт для генерации по референсу",
            "handle_reference_generation_image_upload": "Загрузить референсное изображение",
            "handle_use_current_image_as_reference": "Использовать текущее изображение как референс",
            "handle_remove_reference_generation_image": "Удалить референсное изображение",
            "handle_back_from_custom_generation": "Вернуться из кастомной генерации"
        }
    },
    "ModerationPublicationService": {
        "ru_name": "Сервис модерации публикаций",
        "methods": {
            "handle_navigate_publication": "Навигация по публикации",
            "handle_toggle_social_network": "Переключить социальную сеть",
            "handle_prev_image": "Предыдущее изображение",
            "handle_next_image": "Следующее изображение",
            "handle_publish_now": "Опубликовать сейчас",
            "handle_reject_comment_input": "Ввести комментарий отклонения",
            "handle_send_rejection": "Отправить отклонение",
            "handle_regenerate_text": "Перегенерировать текст",
            "handle_regenerate_text_prompt_input": "Ввести промпт для перегенерации текста",
            "handle_edit_publication_text": "Редактировать текст публикации",
            "handle_generate_new_image": "Сгенерировать новое изображение",
            "handle_edit_image_prompt_input": "Ввести промпт для редактирования изображения",
            "handle_image_upload": "Загрузить изображение",
            "handle_remove_image": "Удалить изображение",
            "handle_save_edits": "Сохранить изменения",
            "handle_back_to_moderation_list": "Вернуться к списку модерации",
            "handle_compress_text": "Сжать текст",
            "handle_remove_photo_from_long_text": "Удалить фото из длинного текста",
            "handle_restore_previous_state": "Восстановить предыдущее состояние",
            "handle_back_to_content_menu": "Вернуться в меню контента",
            "handle_combine_images_start": "Начать объединение изображений",
            "handle_combine_with_current_image": "Объединить с текущим изображением",
            "handle_combine_image_from_scratch": "Объединить изображение с нуля",
            "handle_combine_image_upload": "Загрузить изображение для объединения",
            "handle_prev_combine_image": "Предыдущее объединяемое изображение",
            "handle_next_combine_image": "Следующее объединяемое изображение",
            "handle_back_from_combine_image_upload": "Вернуться из загрузки объединяемого изображения",
            "handle_delete_combine_image": "Удалить объединяемое изображение",
            "handle_combine_image_prompt_input": "Ввести промпт для объединения изображений",
            "handle_skip_combine_image_prompt": "Пропустить промпт для объединения изображений",
            "handle_combine_image_from_new_image": "Объединить изображение из нового изображения",
            "handle_edit_image_prompt_input_from_confirm_new_image": "Ввести промпт для редактирования из подтверждения нового изображения",
            "handle_confirm_new_image": "Подтвердить новое изображение",
            "handle_show_old_image": "Показать старое изображение",
            "handle_show_new_image": "Показать новое изображение",
            "handle_reject_new_image": "Отклонить новое изображение",
            "handle_auto_generate_image": "Автогенерация изображения",
            "handle_reference_generation_image_prompt_input": "Ввести промпт для генерации по референсу",
            "handle_reference_generation_image_upload": "Загрузить референсное изображение",
            "handle_use_current_image_as_reference": "Использовать текущее изображение как референс",
            "handle_remove_reference_generation_image": "Удалить референсное изображение",
            "handle_back_from_custom_generation": "Вернуться из кастомной генерации"
        }
    },
    "IntroService": {
        "ru_name": "Сервис вводного диалога",
        "methods": {
            "accept_user_agreement": "Принять пользовательское соглашение",
            "accept_privacy_policy": "Принять политику конфиденциальности",
            "accept_data_processing": "Принять обработку данных",
            "go_to_create_organization": "Перейти к созданию организации"
        }
    },
    "MainMenuService": {
        "ru_name": "Сервис главного меню",
        "methods": {
            "handle_go_to_content": "Перейти к контенту",
            "handle_text_prompt_input": "Ввести текстовый промпт",
            "handle_go_to_organization": "Перейти к организации",
            "handle_go_to_personal_profile": "Перейти в личный профиль"
        }
    },
    "OrganizationMenuService": {
        "ru_name": "Сервис меню организации",
        "methods": {
            "handle_go_to_employee_settings": "Перейти к настройкам сотрудников",
            "handle_go_to_update_organization": "Перейти к обновлению организации",
            "handle_go_to_update_category": "Перейти к обновлению категории",
            "handle_go_to_add_employee": "Перейти к добавлению сотрудника",
            "handle_go_to_top_up_balance": "Перейти к пополнению баланса",
            "handle_go_to_social_networks": "Перейти к социальным сетям",
            "handle_go_to_main_menu": "Перейти в главное меню"
        }
    },
    "AddEmployeeService": {
        "ru_name": "Сервис добавления сотрудника",
        "methods": {
            "handle_account_id_input": "Ввести ID аккаунта",
            "handle_name_input": "Ввести имя",
            "handle_role_selection": "Выбрать роль",
            "handle_toggle_permission": "Переключить разрешение",
            "handle_create_employee": "Создать сотрудника",
            "handle_go_to_organization_menu": "Перейти в меню организации"
        }
    },
    "PersonalProfileService": {
        "ru_name": "Сервис личного профиля",
        "methods": {
            "handle_go_faq": "Перейти к FAQ",
            "handle_go_to_support": "Перейти в поддержку",
            "handle_back_to_profile": "Вернуться в профиль",
            "handle_go_to_main_menu": "Перейти в главное меню"
        }
    }
}
