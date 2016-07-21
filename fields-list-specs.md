
|  | **Profile Data **  | 
| # | Field name | Frontend label | Type | Default value | Validation | required | Description |
| 1 | first_name | Όνομα | string | - | > 1  | {icon check} | filled with the user's first name |
| 2 | last_name | Επώνυμο | string | - | > 1 | {icon check} | filled with the user's last name |
| 3 | specialty | Ειδικότητα | choices | - | - | {icon check} | the user selects his specialty from a list of choices |
| 4 | kind | Ιδιότητα | choices | - | - | {icon check} | the user selects his kind from a list of choices |
| 5 | tax_reg_num | ΑΦΜ | number | - | tax registration number validation | {icon check} | filled with the user's tax registration number |
| 6 | tax_office | ΔΟΥ | choices | - | - | {icon check} | the user selects his tax office from a list of choices |
| 7 | iban | ΙΒΑΝ | string | - | tax registration number validation | {icon check} | filled with the user's tax registration number |
| 8 | user_category | Κατηγορία Χρήστη | choices (readonly) | B | - | {icon check} | the user should not be able to change it |

| | **Traveler - Petition Data** |
| # | Field name | Frontend label | Type | Default value | Validation | required | Description |
| 1 | first_name | Όνομα | string (readonly) | - | > 1  | {icon check} | filled with the user's first name |
| 2 | last_name | Επώνυμο | string (readonly) | - | > 1 | {icon check} | filled with the user's last name |
| 3 | specialty | Ειδικότητα | choices (readonly) | - | - | {icon check} | the user selects his specialty from a list of choices |
| 4 | kind | Ιδιότητα | choices (readonly) | - | - | {icon check} | the user selects his kind from a list of choices |
| 5 | tax_reg_num | ΑΦΜ | number (readonly) | - | tax registration number validation | {icon check} | filled with the user's tax registration number |
| 6 | tax_office | ΔΟΥ | choices (readonly) | - | - | {icon check} | the user selects his tax office from a list of choices |
| 7 | iban | ΙΒΑΝ | string (readonly) | - | tax registration number validation | {icon check} | filled with the user's tax registration number |
| 8 | user_category | Κατηγορία Χρήστη | choices (readonly) | B | - | {icon check} | the user should not be able to change it |
| 9 | dse | ΔΣΕ | number (readonly) | - | - | {icon check} | auto increment value - filled automatically by the system |
| 10 | project (project manager) | Έργο - Υπεύθυνος Έργου | choices | - | - | {icon check} | the user selects the project related with his trip from a list of choices |
| 11 | reason | Αιτιολογία Μετακίνησης | textarea | - | 5 < [min, max] < determined by the pdf generation process | {icon check} | the user should fill in the reason of his transportation |
| 12 | movement_category | Κατηγορία Μετακίνησης | choices (readonly) | - | - | {icon check} | After the selection of the desired arrival point, this field should take automatically the value ("Εσωτερικό"/"Εξωτερικό") |
| 13 | country_category | Κατηγορία Χώρας | choices (readonly) | - | - | {icon check} | After the selection of the desired arrival point, this field should take automatically the value ("Α/Β/Γ") depending on the category of the selected country |
| 14 | departure_point | Τόπος Μετακίνησης - Από: | choices | ΑΘΗΝΑ | - | {icon check} | the user selects the departure point of his transportation  |
| 15 | arrival_point | Τόπος Προορισμού - Προς: | choices | - | - | {icon check} | the user selects the arrival point of his transportation |
| 16 | task_start_date | Έναρξη Εργασιών | date - time | - | should be after today | {icon check} | the user chooses the starting date and time of the task that is the reason of his transportation |
| 17 | task_end_date | Λήξη Εργασιών | date - time | - | should be after taskStartDate | {icon check} | the user chooses the ending date and time of the task that is the reason of his transportation |
| 18 | depart_date | Αναχώρηση | date - time | - | should be after today | - | the user chooses the departure date and time  of his transportation |
| 19 | return_date | Επιστροφή | date - time | - | should be after taskStartDate | - | the user chooses the return date and time of his transportation |
| 20 | mean_of_transport | Μέσο Μετακίνησης | choices | Αεροπλάνο | - | - |  the user chooses the mean of his transportation |
| 21 | transportation | Τιμή Εισιτηρίου | number | - | > 0 | - | filled with the price of the ticket |
| 22 | accommodation | Τιμή Διανυκτέρευσης (/ημέρα) | number - currency | - | this value should be > 0 and (< 220 if the user belongs in category A or < 160 if the user belongs in category B) + 100 if the arrival point == New York| - | price of accommodation |
| 23 | registration_cost | Κόστος Συμμετοχής | number - currency | - | > 0 | - | filled with the cost of participation in conferences etc. |
| 24 | additional_expenses | Λοιπά Έξοδα Μετακίνησης | number - currency | - | > 0 | - | filled with the additional expenses that may exist due to train/metro/bus tickets etc. |
| 25 | meals | Κάλυψη Διατροφής | choices | (-) | - | - | the user may choose among none (-), breakfast, half board or full board |
| 26 | non_grnet_quota | Κάλυψη Ημερήσιας Αποζημίωσης από άλλο Φορέα | number | - | > 0 | - | filled with the amount being paid by another carrier |
| 27 | user_recommendation | Αρχικές Προτάσεις Μετακινούμενου (για κρατήσεις πτήσεων, ξενοδοχείου, κλπ) | textarea | - | - | - | the user should fill this field with his suggestion concerning the type of accommodation (hotel, airbnb etc.) and the transportation(arrival/departure time, airline company etc.) |

|  | **Secretary - Petition Data** |
| # | Field name | Frontend label | Type | Default value | Validation | required | Description |
| 1 | first_name | Όνομα | string | - | > 1  | {icon check} | filled with the user's first name |
| 2 | last_name | Επώνυμο | string | - | > 1 | {icon check} | filled with the user's last name |
| 3 | specialty | Ειδικότητα | choices | - | - | {icon check} | the user selects his specialty from a list of choices |
| 4 | kind | Ιδιότητα | choices | - | - | {icon check} | the user selects his kind from a list of choices |
| 5 | tax_reg_num | ΑΦΜ | number | - | tax registration number validation | {icon check} | filled with the user's tax registration number |
| 6 | tax_office | ΔΟΥ | choices | - | - | {icon check} | the user selects his tax office from a list of choices |
| 7 | iban | ΙΒΑΝ | string | - | tax registration number validation | {icon check} | filled with the user's tax registration number |
| 8 | user_category | Κατηγορία Χρήστη | choices | B | - | {icon check} | the user should not be able to change it |
| 9 | dse | ΔΣΕ | number (readonly) | - | - | {icon check} | auto increment value - filled automatically by the system |
| 10 | project (project manager) | Έργο | choices | - | - | {icon check} | the user selects the project related with his trip from a list of choices |
| 11 | reason | Αιτιολογία Μετακίνησης | textarea | - | 5 < [min, max] < determined by the pdf generation process | {icon check} | the user should fill in the reason of his transportation |
| 12 | movement_category | Κατηγορία Μετακίνησης | choices (readonly) | - | - | {icon check} | After the selection of the desired arrival point, this field should take automatically the value ("Εσωτερικό"/"Εξωτερικό") |
| 13 | country_category | Κατηγορία Χώρας | choices (readonly) | - | - | {icon check} | After the selection of the desired arrival point, this field should take automatically the value ("Α/Β/Γ") depending on the category of the selected country |
| 14 | departure_point | Τόπος Μετακίνησης - Από: | choices | ΑΘΗΝΑ | - | {icon check} | the user selects the departure point of his transportation  |
| 15 | arrival_point | Τόπος Προορισμού - Προς: | choices | - | - | {icon check} | the user selects the arrival point of his transportation |
| 16 | task_start_date | Έναρξη Εργασιών | date - time | - | should be after today | {icon check} | the user chooses the starting date and time of the task that is the reason of his transportation |
| 17 | task_end_date | Λήξη Εργασιών | date - time | - | should be after taskStartDate | {icon check} | the user chooses the ending date and time of the task that is the reason of his transportation |
| 18 | depart_date | Αναχώρηση | date - time | - | should be after today | {icon check} | the user chooses the departure date and time  of his transportation |
| 19 | return_date | Επιστροφή | date - time | - | should be after departDate and taskStartDate | {icon check} | the user chooses the return date and time of his transportation |
| 20 | mean_of_transport | Μέσο Μετακίνησης | choices | Αεροπλάνο | - | {icon check} |  the user chooses the mean of his transportation |
| 21 | transportation | Τιμή Εισιτηρίου | number | - | > 0 | {icon check} | filled with the price of the ticket |
| 22 | accommodation | Τιμή Διανυκτέρευσης (/ημέρα) | number - currency | - | this value should be > 0 and (< 220 if the user belongs in category A or < 160 if the user belongs in category B) + 100 if the arrival point == New York| {icon check} | price of accommodation |
| 23 | registration_cost | Κόστος Συμμετοχής | number - currency | - | > 0 | - | filled with the cost of participation in conferences etc. |
| 24 | additional_expenses | Λοιπά Έξοδα Μετακίνησης | number - currency | - | > 0 | - | filled with the additional expenses that may exist due to train/metro/bus tickets etc. |
| 25 | meals | Κάλυψη Διατροφής | choices | (-) | - | - | the user may choose among none (-), breakfast, half board or full board |
| 26 | non_grnet_quota | Κάλυψη Ημερήσιας Αποζημίωσης από άλλο Φορέα | number | - | > 0 | - | filled with the amount being paid by another carrier |
| 27 | travel_data | Στοιχεία σχετικά με την μετακίνηση και τη διαμονή | textarea | - | - | - | the user should fill this field with the final infos concerning the type of the accommodation (hotel, airbnb etc.) and the transportation(arrival/departure time, airline company etc.) |
| 28 | movement_id| Αρ.Μετακίνησης | string | - | - | {icon check} | the value of this field is the name of the petition's project + the current year + the serial number of this project's transportation (e.g. PRACE4IP/2016/1) |
| 28 | expenditure_date_protocol | Ημ. Πρ. Αίτησης Δαπάνης Μετακίνησης | date | - | should be after today | {icon check} | filled by the protocol's export date |
| 29 | expenditure_protocol | Αρ. Πρ. Αίτησης Δαπάνης Μετακίνησης | number | - | - | {icon check} | filled by the protocol's export number |
| 30 | movement_date_protocol | Ημ. Πρ. Απόφασης Μετακίνησης | date | - | should be after today | {icon check} | filled by the protocol's export date |
| 31 | movement_protocol | Αρ. Πρ. Απόφασης Μετακίνησης | number | - | - | {icon check} | filled by the protocol's export number |
| 32 | transport_days_manual | Ημέρες Μετακίνησης Εργασιών | number | - | - | {icon check} | equals (return_date - depart_date) - Weekends - Holidays. This value is proposed by the system and could be changed by the user |
| 33 | transport_days_proposed | Ημέρες Μετακίνησης Εργασιών (προτεινόμενη τιμή) | number (readonly) | - | - | {icon check} | equals (returnDate - departDate) - Weekends - Holidays. This value is proposed by the system |
| 34 | overnights_num_manual | Διανυκτερεύσεις | number  | - | - | {icon check} | this field represents the sum of overnights proposed by the system and could be changed by the user|
| 35 | overnights_num_proposed | Διανυκτερεύσεις (προτεινόμενη τιμή) | number (readonly) | - | - | {icon check} | this field represents the sum of overnights proposed by the system |
| 36 | compensation_days_manual | Ημέρες Αποζημίωσης | number | - | - | {icon check} | equals (task_end_date - task_start_date) + depart_date. This value is proposed by the system and could be changed by the user |
| 37 | compensation_days_proposed | Ημέρες Αποζημίωσης (προτεινόμενη τιμή) (readonly) | number | - | - | {icon check} | equals (task_end_date - task_start_date) + depart_date. This value is proposed by the system |
| 38 | same_day_return_task | Αυθημερόν Επιστροφή | boolean | false | check if depart_date == return_date | {icon check} | automatically filled by the system |
| 39 | trip_days_before | Εναπομείνασες Ημέρες Μετακίνησης Εργασιών: Πριν | number (readonly) | 60 | < 60 | {icon check} | trip days assigned to the employee before his transportation |
| 40 | trip_days_after | Εναπομ. Ημ. Μετακ. Εργ.: Μετά | number (readonly) | - | < 60 | {icon check} | trip days remained to the employee after his transportation |
| 41 | overnights_sum_cost | Σύνολο Διανυκτέρευσης | number (readonly) | - | - | {icon check} | equals  overnights_num_manual * accommodation |
| 42 | compensation_level | Αποζημίωση (Ημερήσια) | number (readonly) | - | - | {icon check} | the amount of the daily compensation which is determined by the user's and the country's category (*see table "Daily Compensation" below) |
| 43 | compensation_final | Σύνολο Ημερήσιας Αποζημίωσης | number (readonly) | - | - | {icon check} | equals compensation_days_manual * compensation_level |
| 44 | total_cost | ΣΥΝΟΛΟ | number (readonly) | - | - | {icon check} | equals in general compensation_final + overnights_sum_cost + transportation + additional_expenses + non_grnet_quota (for more details see below) |

|Daily Compensation|
| Country Category | Α | Β | Γ |
| User Category Ι | 100 € | 80 € | 60 € |
| User Category ΙΙ | 80 € | 60 € | 50 € |

| Daily Compensation - Rules |
| 1 | Η ημερήσια αποζημίωση καταβάλλεται **ολόκληρη** | Για την ημέρα μετάβασης και επιστροφής, όταν αυτή συμπίπτει με τη λήξη εργασιών | για κάθε ημέρα παραμονής και διανυκτέρευσης |
| 2 | Καταβάλλεται **μειωμένη κατά 50%** | η επιστροφή πραγματοποιείται αυθημερόν (same_day_return_task == true) | στην περίπτωση που παρέχεται ημιδιατροφή (meals == half board) |
| 3 | Καταβάλλεται **μειωμένη κατά 75%** | καλύπτονται τα έξοδα διατροφής και διανυκτέρευσης (meals == full board) | |
| 4 | Σε περίπτωση κάλυψης μέρους της αποζημίωσης από άλλον φορέα, καταβάλλεται το υπόλοιπο του ποσού που δικαιούται ο μετακινούμενος (compensation_final = compensation_final - compensation_final*non_grnet_quota ) | | |

| Petition States | Label | Description | Petition Status Transitions |
| 1 | Σε επεξεργασία από τον μετακινούμενο | when the simple user create or edit a petition | |
| 2 | Υποβεβλημένη από τον μετακινούμενο | when the simple user submits a petition | |
|   |  |  |  2 --> 1 : the user can cancel the submission of the petition if the secretary haven't edit the petition yet |
| 3 | Σε επεξεργασία από τη γραμματεία | when the secretary saves the petition for the 1st time and until she submit it | |
| 4 | Οριστικοποιημένη από τη γραμματεία | when the secretary submits the petition | |
| 5 | Απόφαση Μετακίνησης για ανάρτηση στη ΔΙΑΥΓΕΙΑ | | |
| 6 | Απόφαση Μετακίνησης υπογεγραμμένη από τον Πρόεδρο | | |
| 7 | Σε επεξεργασία από μετακινούμενο για αποζημίωση | | |
| 8 | Υποβεβλημένη από τον μετακινούμενο για αποζημίωση | | |
| 9 | Σε επεξεργασία από τον Υπεύθυνο Μετακινήσεων | | |
| 10 | Οριστικοποιημένη από τον Υπεύθυνο Μετακινήσεων | | |
| 11 | Απόφαση Αποζημίωσης για ανάρτηση στη ΔΙΑΥΓΕΙΑ | | |
| 12 | Απόφαση Αποζημίωσης υπογεγραμμένη από τον Πρόεδρο | | |
| 13 | Ολοκληρωμένη | | |
| 14 | Ακυρωμένη | | |
