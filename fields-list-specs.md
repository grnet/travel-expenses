# BOLD fields are exposed to the user

|  | **Profile Data**  |
| # | Field name | Frontend label | Type | Default value | Validation | required | Description |
| 1 | **first_name** | Όνομα | string | - | > 1  | {icon check} | filled with the user's first name |
| 2 | **last_name** | Επώνυμο | string | - | > 1 | {icon check} | filled with the user's last name |
| 3 | **specialty** | Ειδικότητα | choices | - | - | {icon check} | the user selects his specialty from a list of choices |
| 4 | **kind** | Ιδιότητα | choices | - | - | {icon check} | the user selects his kind from a list of choices |
| 5 | **tax_reg_num** | ΑΦΜ | number | - | tax registration number validation | {icon check} | filled with the user's tax registration number |
| 6 | **tax_office** | ΔΟΥ | choices | - | - | {icon check} | the user selects his tax office from a list of choices |
| 7 | **iban** | ΙΒΑΝ | string | - | tax registration number validation | {icon check} | filled with the user's tax registration number |
| 8 | **user_category** | Κατηγορία Χρήστη | choices (readonly) | B | - | {icon check} | the user should not be able to change it |
| 9 | user_group |  | choices | - | - | {icon check} | this field describes the group in which the user belongs to |
| 10 | trip_days_left |  | number | 60 | <=60 | {icon check} | trip days remained to the employee before his transportation |
| 11 | **username** | username | string |  | unique | {icon check} | the username of the user |

| | **Traveler - Petition Data** |
| # | Field name | Frontend label | Type | Default value | Validation | required | Description |
| 1 | **first_name** | Όνομα | string (readonly) | - | > 1  | {icon check} | filled with the user's first name |
| 2 | **last_name** | Επώνυμο | string (readonly) | - | > 1 | {icon check} | filled with the user's last name |
| 3 | **specialty** | Ειδικότητα | choices (readonly) | - | - | {icon check} | the user selects his specialty from a list of choices |
| 4 | **kind** | Ιδιότητα | choices (readonly) | - | - | {icon check} | the user selects his kind from a list of choices |
| 5 | **tax_reg_num** | ΑΦΜ | number (readonly) | - | tax registration number validation | {icon check} | filled with the user's tax registration number |
| 6 | **tax_office** | ΔΟΥ | choices (readonly) | - | - | {icon check} | the user selects his tax office from a list of choices |
| 7 | **iban** | ΙΒΑΝ | string (readonly) | - | tax registration number validation | {icon check} | filled with the user's tax registration number |
| 8 | **user_category** | Κατηγορία Χρήστη | choices (readonly) | B | - | {icon check} | the user should not be able to change it |
| 9 | **dse** | ΔΣΕ | number (readonly) | - | - | {icon check} | auto increment value - filled automatically by the system |
| 10 | **project (project manager)** | Έργο - Υπεύθυνος Έργου | choices | - | - | {icon check} | the user selects the project related with his trip from a list of choices |
| 11 | **reason** | Αιτιολογία Μετακίνησης | textarea | - | 5 < [min, max] < determined by the pdf generation process | {icon check} | the user should fill in the reason of his transportation |
| 12 | **movement_category** | Κατηγορία Μετακίνησης | choices (readonly) | - | - | {icon check} | After the selection of the desired arrival point, this field should take automatically the value ("Εσωτερικό"/"Εξωτερικό") |
| 13 | **country_category** | Κατηγορία Χώρας | choices (readonly) | - | - | {icon check} | After the selection of the desired arrival point, this field should take automatically the value ("Α/Β/Γ") depending on the category of the selected country |
| 14 | **departure_point** | Τόπος Μετακίνησης - Από: | choices | ΑΘΗΝΑ | - | {icon check} | the user selects the departure point of his transportation  |
| 15 | **arrival_point** | Τόπος Προορισμού - Προς: | choices | - | - | {icon check} | the user selects the arrival point of his transportation |
| 16 | **task_start_date** | Έναρξη Εργασιών | date - time | - | should be after today | {icon check} | the user chooses the starting date and time of the task that is the reason of his transportation |
| 17 | **task_end_date** | Λήξη Εργασιών | date - time | - | should be after taskStartDate | {icon check} | the user chooses the ending date and time of the task that is the reason of his transportation |
| 18 | **depart_date** | Αναχώρηση | date - time | - | should be after today | - | the user chooses the departure date and time  of his transportation |
| 19 | **return_date** | Επιστροφή | date - time | - | should be after taskStartDate | - | the user chooses the return date and time of his transportation |
| 20 | **means_of_transport** | Μέσο Μετακίνησης | choices | Αεροπλάνο | - | - |  the user chooses the mean of his transportation |
| 21 | **transportation_cost** | Τιμή Εισιτηρίου | number | - | > 0 | - | filled with the cost of the ticket |
| 22 | **accommodation_local_cost** | Τιμή Διανυκτέρευσης (/ημέρα) | number - currency | - | this value should be > 0 and (< 220 if the user belongs in category A or < 160 if the user belongs in category B) + 100 if the arrival point == New York| - | cost of accommodation in local currency (€, $ etc.) |
| 23 | **participation_local_cost** | Κόστος Συμμετοχής | number - currency | - | > 0 | - | filled with the cost of participation in conferences etc. in local currency (€, $ etc.) |
| 24 | **additional_expenses_initial** | Λοιπά Έξοδα Μετακίνησης | number - currency | - | > 0 | - | filled with the additional expenses that may exist due to train/metro/bus tickets etc. |
| 25 | **meals** | Κάλυψη Διατροφής | choices | (-) | - | - | the user may choose among none (-), breakfast, half board or full board |
| 26 | **additional_expenses_initial_description** | Λοιπά Έξοδα Μετακίνησης - Περιγραφή | textarea | - | 5 < [min, max] < determined by the pdf generation process | - | filled with the description of additional expenses that may exist due to train/metro/bus tickets etc. |
| 27 | **user_recommendation** | Αρχικές Προτάσεις Μετακινούμενου (για κρατήσεις πτήσεων, ξενοδοχείου, κλπ) | textarea | - | 5 < [min, max] < determined by the pdf generation process | - | the user should fill this field with his suggestion concerning the type of accommodation (hotel, airbnb etc.) and the transportation(arrival/departure time, airline company etc.) |

|  | **Secretary - Petition Data** |
| # | Field name | Frontend label | Type | Default value | Validation | required | Description |
| 1 | **first_name** | Όνομα | string | - | > 1  | {icon check} | filled with the user's first name |
| 2 | **last_name** | Επώνυμο | string | - | > 1 | {icon check} | filled with the user's last name |
| 3 | **specialty** | Ειδικότητα | choices | - | - | {icon check} | the user selects his specialty from a list of choices |
| 4 | **kind** | Ιδιότητα | choices | - | - | {icon check} | the user selects his kind from a list of choices |
| 5 | **tax_reg_num** | ΑΦΜ | number | - | tax registration number validation | {icon check} | filled with the user's tax registration number |
| 6 | **tax_office** | ΔΟΥ | choices | - | - | {icon check} | the user selects his tax office from a list of choices |
| 7 | **iban** | ΙΒΑΝ | string | - | tax registration number validation | {icon check} | filled with the user's tax registration number |
| 8 | **user_category** | Κατηγορία Χρήστη | choices | B | - | {icon check} | the user should not be able to change it |
| 9 | **dse** | ΔΣΕ | number (readonly) | - | - | {icon check} | auto increment value - filled automatically by the system |
| 10 | **project** (project manager) | Έργο | choices | - | - | {icon check} | the user selects the project related with his trip from a list of choices |
| 11 | **reason** | Αιτιολογία Μετακίνησης | textarea | - | 5 < [min, max] < determined by the pdf generation process | {icon check} | the user should fill in the reason of his transportation |
| 12 | **movement_category** | Κατηγορία Μετακίνησης | choices (readonly) | - | - | {icon check} | After the selection of the desired arrival point, this field should take automatically the value ("Εσωτερικό"/"Εξωτερικό") |
| 13 | **country_category** | Κατηγορία Χώρας | choices (readonly) | - | - | {icon check} | After the selection of the desired arrival point, this field should take automatically the value ("Α/Β/Γ") depending on the category of the selected country |
| 14 | **departure_point** | Τόπος Μετακίνησης - Από: | choices | ΑΘΗΝΑ | - | {icon check} | the user selects the departure point of his transportation  |
| 15 | **arrival_point** | Τόπος Προορισμού - Προς: | choices | - | - | {icon check} | the user selects the arrival point of his transportation |
| 16 | **task_start_date** | Έναρξη Εργασιών | date - time | - | should be after today | {icon check} | the user chooses the starting date and time of the task that is the reason of his transportation |
| 17 | **task_end_date** | Λήξη Εργασιών | date - time | - | should be after taskStartDate | {icon check} | the user chooses the ending date and time of the task that is the reason of his transportation |
| 18 | **depart_date** | Αναχώρηση | date - time | - | should be after today | {icon check} | the user chooses the departure date and time  of his transportation |
| 19 | **return_date** | Επιστροφή | date - time | - | should be after departDate and taskStartDate | {icon check} | the user chooses the return date and time of his transportation |
| 20 | **means_of_transport** | Μέσο Μετακίνησης | choices | Αεροπλάνο | - | {icon check} |  the user chooses the mean of his transportation |
| 21 | **transportation_cost** | Τιμή Εισιτηρίου | number | - | > 0 | {icon check} | filled with the cost of the ticket |
| 22 | transportation_default_currency | - | char | - | - | {icon check} | the default currency in which the cost of transportation will be saved (€) |
| 23 | **transportation_payment_way** | Πληρωμή | choices | - | - | {icon check} | choices of payment ways credit card, travel agency etc |
| 24 | **transportation_payment_description** | Περιγραφή | textarea | - | 5 < [min, max] < determined by the pdf generation process | {icon check} | description of the payment |
| 25 | **accommodation_local_cost** | Τιμή Διανυκτέρευσης (/ημέρα) | number - currency | > 0 | this value should be > 0 and (< 220 if the user belongs in category A or < 160 if the user belongs in category B) + 100 if the arrival point == New York| {icon check} | cost of accommodation in local currency (€, $ etc.) |
| 26 | **accommodation_cost** | Τιμή Διανυκτέρευσης (/ημέρα) | number - currency | - | this value should be > 0 and (< 220 if the user belongs in category A or < 160 if the user belongs in category B) + 100 if the arrival point == New York| {icon check} | cost of accommodation in € |
| 27 | accommodation_default_currency | - | char | - | - | {icon check} | the default currency in which the cost of accommodation will be saved (€) |
| 28 | accommodation_local_currency | - | char | - | - | {icon check} | the local currency in which the cost of accommodation will be saved |
| 29 | **accommodation_payment_way** | Πληρωμή | choices | - | - | {icon check} | choices of payment ways credit card, travel agency etc |
| 30 | **accommodation_payment_description** | Περιγραφή | textarea | - | 5 < [min, max] < determined by the pdf generation process | {icon check} | description of the payment |
| 31 | **participation_local_cost** | Κόστος Συμμετοχής | number - currency | - | > 0 | {icon check} | filled with the cost of participation in conferences etc. in local currency (€, $ etc.) |
| 32 | **participation_cost** | Κόστος Συμμετοχής | number - currency | - | > 0 | {icon check} | filled with the cost of participation in conferences etc. in € |
| 33 | participation_default_currency | - | char | - | - | {icon check} | the default currency in which the cost of participation will be saved (€)|
| 34 | participation_local_currency | - | char | - | - | {icon check} | the local currency in which the cost of participation will be saved |
| 35 | **participation_payment_way** | Πληρωμή | choices | - | - | {icon check} | choices of payment ways credit card, travel agency etc |
| 36 | **participation_payment_description** | Περιγραφή | textarea | - | 5 < [min, max] < determined by the pdf generation process | {icon check} | description of the payment |
| 37 | **additional_expenses_initial** | Λοιπά Έξοδα Μετακίνησης | number - currency | - | > 0 | - | filled with the additional expenses that may exist due to train/metro/bus tickets etc. |
| 33 | additional_expenses_default_currency | - | char | - | - | {icon check} | the default currency in which additional_expenses will be saved (€)|
| 37 | **additional_expenses_initial_description** | Περιγραφή | textarea | - | 5 < [min, max] < determined by the pdf generation process | - | filled with the description of additional expenses |
| 38 | **meals** | Κάλυψη Διατροφής | choices | (-) | - | {icon check} | the user may choose among none (-), breakfast, half board or full board |
| 39 | **non_grnet_quota** | Κάλυψη Ημερήσιας Αποζημίωσης από άλλο Φορέα | number | - | > 0 | - | filled with the amount being paid by another carrier |
| 40 | **travel_data** | Στοιχεία σχετικά με την μετακίνηση και τη διαμονή | textarea | - | 5 < [min, max] < determined by the pdf generation process | - | the user should fill this field with the final infos concerning the type of the accommodation (hotel, airbnb etc.) and the transportation(arrival/departure time, airline company etc.) |
| 41 | **movement_id** | Αρ.Μετακίνησης | string | - | - | {icon check} | the value of this field is the name of the petition's project + the current year + the serial number of this project's transportation (e.g. PRACE4IP/2016/1) |
| 42 | **expenditure_date_protocol** | Ημ. Πρ. Αίτησης Δαπάνης Μετακίνησης | date | - | should be after today | {icon check} | filled by the protocol's export date |
| 43 | **expenditure_protocol** | Αρ. Πρ. Αίτησης Δαπάνης Μετακίνησης | number | - | - | {icon check} | filled by the protocol's export number |
| 44 | **movement_date_protocol** | Ημ. Πρ. Απόφασης Μετακίνησης | date | - | should be after today | {icon check} | filled by the protocol's export date |
| 45 | **movement_protocol** | Αρ. Πρ. Απόφασης Μετακίνησης | number | - | - | {icon check} | filled by the protocol's export number |
| 46 | **transport_days_manual** | Ημέρες Μετακίνησης Εργασιών | number | - | - | {icon check} | equals (return_date - depart_date) - Weekends - Holidays. This value is proposed by the system and could be changed by the user |
| 47 | **transport_days_proposed** | Ημέρες Μετακίνησης Εργασιών (προτεινόμενη τιμή) | number (readonly) | - | - | {icon check} | equals (returnDate - departDate) - Weekends - Holidays. This value is proposed by the system |
| 48 | **overnights_num_manual** | Διανυκτερεύσεις | number  | - | - | {icon check} | this field represents the sum of overnights proposed by the system and could be changed by the user|
| 49 | **overnights_num_proposed** | Διανυκτερεύσεις (προτεινόμενη τιμή) | number (readonly) | - | - | {icon check} | this field represents the sum of overnights proposed by the system |
| 50 | **compensation_days_manual** | Ημέρες Αποζημίωσης | number | - | - | {icon check} | equals (task_end_date - task_start_date) + depart_date. This value is proposed by the system and could be changed by the user |
| 51 | **compensation_days_proposed** | Ημέρες Αποζημίωσης (προτεινόμενη τιμή) (readonly) | number | - | - | {icon check} | equals (task_end_date - task_start_date) + depart_date. This value is proposed by the system |
| 52 | **same_day_return_task** | Αυθημερόν Επιστροφή | boolean | false | check if depart_date == return_date | {icon check} | automatically filled by the system |
| 53 | **trip_days_before** | Εναπομείνασες Ημέρες Μετακίνησης Εργασιών: Πριν | number (readonly) | 60 | < 60 | {icon check} | trip days assigned to the employee before his transportation |
| 54 | **trip_days_after** | Εναπομ. Ημ. Μετακ. Εργ.: Μετά | number (readonly) | - | < 60 | {icon check} | trip days remained to the employee after his transportation |
| 55 | **overnights_sum_cost** | Σύνολο Διανυκτέρευσης | number (readonly) | - | - | {icon check} | equals  overnights_num_manual * accommodation |
| 56 | **compensation_level** | Αποζημίωση (Ημερήσια) | number (readonly) | - | - | {icon check} | the amount of the daily compensation which is determined by the user's and the country's category (*see table "Daily Compensation" below) |
| 57 | **compensation_final** | Σύνολο Ημερήσιας Αποζημίωσης | number (readonly) | - | - | {icon check} | equals compensation_days_manual * compensation_level |
| 58 | **total_cost** | ΣΥΝΟΛΟ | number (readonly) | - | - | {icon check} | equals in general compensation_final + overnights_sum_cost + transportation + additional_expenses + non_grnet_quota (for more details see below) |

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

|List of tax_reg_num for testing purposes|
|135362340|
|117974430|
|047823892|
|022790563|
|156203378|