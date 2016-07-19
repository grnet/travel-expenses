
|  | **Profile Data **  | 
| # | Field name | Frontend label | Type | Default value | Validation | required | Description |
| 1 | name | Όνομα | string | - | > 1  | - | filled with the user's first name |
| 2 | surname | Επώνυμο | string | - | > 1 | - | filled with the user's last name |
| 3 | specialty | Ειδικότητα | choices | - | - | - | the user selects his specialty from a list of choices |
| 4 | kind | Ιδιότητα | choices | - | - | - | the user selects his kind from a list of choices |
| 5 | taxRegNum | ΑΦΜ | number | - | tax registration number validation | - | filled with the user's tax registration number |
| 6 | taxOffice | ΔΟΥ | choices | - | - | - | the user selects his tax office from a list of choices |
| 7 | iban | ΙΒΑΝ | string | - | tax registration number validation | - | filled with the user's tax registration number |
| 8 | userCategory | Κατηγορία Χρήστη | choices (readonly) | B | - | - | the user should not be able to change it |

| | **Traveler - Petition Data** |
| # | Field name | Frontend label | Type | Default value | Validation | required | Description |
| 1 | name | Όνομα | string | - | > 1  | {icon check} | filled with the user's first name |
| 2 | surname | Επώνυμο | string | - | > 1 | {icon check} | filled with the user's last name |
| 3 | specialty | Ειδικότητα | choices | - | - | {icon check} | the user selects his specialty from a list of choices |
| 4 | kind | Ιδιότητα | choices | - | - | {icon check} | the user selects his kind from a list of choices |
| 5 | taxRegNum | ΑΦΜ | number | - | tax registration number validation | {icon check} | filled with the user's tax registration number |
| 6 | taxOffice | ΔΟΥ | choices | - | - | {icon check} | the user selects his tax office from a list of choices |
| 7 | iban | ΙΒΑΝ | string | - | tax registration number validation | {icon check} | filled with the user's tax registration number |
| 8 | userCategory | Κατηγορία Χρήστη | choices (readonly) | B | - | {icon check} | the user should not be able to change it |
| 9 | dse | ΔΣΕ | number (readonly) | - | - | {icon check} | auto increment value - filled automatically by the system |
| 10 | project (project manager) | Έργο - Υπεύθυνος Έργου | choices | - | - | {icon check} | the user selects the project related with his trip from a list of choices |
| 11 | reason | Αιτιολογία Μετακίνησης | textarea | - | 5 < [min, max] < determined by the pdf generation process | {icon check} | the user should fill in the reason of his transportation |
| 12 | movementCategory | Κατηγορία Μετακίνησης | choices (readonly) | - | - | {icon check} | After the selection of the desired arrival point, this field should take automatically the value ("Εσωτερικό"/"Εξωτερικό") |
| 13 | countryCategory | Κατηγορία Χώρας | choices (readonly) | - | - | {icon check} | After the selection of the desired arrival point, this field should take automatically the value ("Α/Β/Γ") depending on the category of the selected country |
| 14 | departurePoint | Τόπος Μετακίνησης - Από: | choices | ΑΘΗΝΑ | - | {icon check} | the user selects the departure point of his transportation  |
| 15 | arrivalPoint | Τόπος Προορισμού - Προς: | choices | - | - | {icon check} | the user selects the arrival point of his transportation |
| 16 | taskStartDate | Έναρξη Εργασιών | date - time | - | should be after today | {icon check} | the user chooses the starting date and time of the task that is the reason of his transportation |
| 17 | taskEndDate | Λήξη Εργασιών | date - time | - | should be after taskStartDate | {icon check} | the user chooses the ending date and time of the task that is the reason of his transportation |
| 18 | departDate | Αναχώρηση | date - time | - | should be after today | - | the user chooses the departure date and time  of his transportation |
| 19 | returnDate | Επιστροφή | date - time | - | should be after taskStartDate | - | the user chooses the return date and time of his transportation |
| 20 | meanOfTransport | Μέσο Μετακίνησης | choices | Αεροπλάνο | - | - |  the user chooses the mean of his transportation |
| 21 | transportation | Τιμή Εισιτηρίου | number | - | > 0 | - | filled with the price of the ticket |
| 22 | accommodation | Τιμή Διανυκτέρευσης (/ημέρα) | number - currency | - | this value should be > 0 and (< 220 if the user belongs in category A or < 160 if the user belongs in category B) + 100 if the arrival point == New York| - | price of accommodation |
| 23 | registrationCost | Κόστος Συμμετοχής | number - currency | - | > 0 | - | filled with the cost of participation in conferences etc. |
| 24 | additionalExpenses | Λοιπά Έξοδα Μετακίνησης | number - currency | - | > 0 | - | filled with the additional expenses that may exist due to train/metro/bus tickets etc. |
| 25 | food | Κάλυψη Διατροφής | choices | (-) | - | - | the user may choose among half board, full board or none (-) |
| 26 | nonGrnetQuota | Κάλυψη Ημερήσιας Αποζημίωσης από άλλο Φορέα | number | - | > 0 | - | filled with the amount being paid by another carrier |
| 27 | userRecommendation | Αρχικές Προτάσεις Μετακινούμενου (για κρατήσεις πτήσεων, ξενοδοχείου, κλπ) | textarea | - | - | - | the user should fill this field with his suggestion concerning the type of accommodation (hotel, airbnb etc.) and the transportation(arrival/departure time, airline company etc.) |

|  | **Secretary - Petition Data** |
| # | Field name | Frontend label | Type | Default value | Validation | required | Description |
| 1 | name | Όνομα | string | - | > 1  | {icon check} | filled with the user's first name |
| 2 | surname | Επώνυμο | string | - | > 1 | {icon check} | filled with the user's last name |
| 3 | specialty | Ειδικότητα | choices | - | - | {icon check} | the user selects his specialty from a list of choices |
| 4 | kind | Ιδιότητα | choices | - | - | {icon check} | the user selects his kind from a list of choices |
| 5 | taxRegNum | ΑΦΜ | number | - | tax registration number validation | {icon check} | filled with the user's tax registration number |
| 6 | taxOffice | ΔΟΥ | choices | - | - | {icon check} | the user selects his tax office from a list of choices |
| 7 | iban | ΙΒΑΝ | string | - | tax registration number validation | {icon check} | filled with the user's tax registration number |
| 8 | userCategory | Κατηγορία Χρήστη | choices | B | - | {icon check} | the user should not be able to change it |
| 9 | dse | ΔΣΕ | number (readonly) | - | - | {icon check} | auto increment value - filled automatically by the system |
| 10 | project - project manager | Έργο | choices | - | - | {icon check} | the user selects the project related with his trip from a list of choices |
| 11 | reason | Αιτιολογία Μετακίνησης | textarea | - | 5 < [min, max] < determined by the pdf generation process | {icon check} | the user should fill in the reason of his transportation |
| 12 | movementCategory | Κατηγορία Μετακίνησης | choices (readonly) | - | - | {icon check} | After the selection of the desired arrival point, this field should take automatically the value ("Εσωτερικό"/"Εξωτερικό") |
| 13 | countryCategory | Κατηγορία Χώρας | choices (readonly) | - | - | {icon check} | After the selection of the desired arrival point, this field should take automatically the value ("Α/Β/Γ") depending on the category of the selected country |
| 14 | departurePoint | Τόπος Μετακίνησης - Από: | choices | ΑΘΗΝΑ | - | {icon check} | the user selects the departure point of his transportation  |
| 15 | arrivalPoint | Τόπος Προορισμού - Προς: | choices | - | - | {icon check} | the user selects the arrival point of his transportation |
| 16 | taskStartDate | Έναρξη Εργασιών | date - time | - | should be after today | {icon check} | the user chooses the starting date and time of the task that is the reason of his transportation |
| 17 | taskEndDate | Λήξη Εργασιών | date - time | - | should be after taskStartDate | {icon check} | the user chooses the ending date and time of the task that is the reason of his transportation |
| 18 | departDate | Αναχώρηση | date - time | - | should be after today | {icon check} | the user chooses the departure date and time  of his transportation |
| 19 | returnDate | Επιστροφή | date - time | - | should be after departDate and taskStartDate | {icon check} | the user chooses the return date and time of his transportation |
| 20 | meanOfTransport | Μέσο Μετακίνησης | choices | Αεροπλάνο | - | {icon check} |  the user chooses the mean of his transportation |
| 21 | transportation | Τιμή Εισιτηρίου | number | - | > 0 | {icon check} | filled with the price of the ticket |
| 22 | accommodation | Τιμή Διανυκτέρευσης (/ημέρα) | number - currency | - | this value should be > 0 and (< 220 if the user belongs in category A or < 160 if the user belongs in category B) + 100 if the arrival point == New York| {icon check} | price of accommodation |
| 23 | registrationCost | Κόστος Συμμετοχής | number - currency | - | > 0 | - | filled with the cost of participation in conferences etc. |
| 24 | additionalExpenses | Λοιπά Έξοδα Μετακίνησης | number - currency | - | > 0 | - | filled with the additional expenses that may exist due to train/metro/bus tickets etc. |
| 25 | food | Κάλυψη Διατροφής | choices | (-) | - | {icon check} | the user may choose among half board, full board or none (-) |
| 26 | nonGrnetQuota | Κάλυψη Ημερήσιας Αποζημίωσης από άλλο Φορέα | number | - | > 0 | - | filled with the amount being paid by another carrier |
| 27 | travelData | Στοιχεία σχετικά με την μετακίνηση και τη διαμονή | textarea | - | - | - | the user should fill this field with the final infos concerning the type of the accommodation (hotel, airbnb etc.) and the transportation(arrival/departure time, airline company etc.) |
| 28 | movementId| Αρ.Μετακίνησης | string | - | - | {icon check} | the value of this field is the name of the petition's project + the current year + the serial number of this project's transportation (e.g. PRACE4IP/2016/1) |
| 28 | expenditureDateProtocol | Ημ. Πρ. Αίτησης Δαπάνης Μετακίνησης | date | - | should be after today | {icon check} | filled by the protocol's export date |
| 29 | expenditureProtocol | Αρ. Πρ. Αίτησης Δαπάνης Μετακίνησης | number | - | - | {icon check} | filled by the protocol's export number |
| 30 | movementDateProtocol | Ημ. Πρ. Απόφασης Μετακίνησης | date | - | should be after today | {icon check} | filled by the protocol's export date |
| 31 | movementProtocol | Αρ. Πρ. Απόφασης Μετακίνησης | number | - | - | {icon check} | filled by the protocol's export number |
| 32 | transportDaysManual | Ημέρες Μετακίνησης Εργασιών | number | - | - | {icon check} | equals (returnDate - departDate) - Weekends - Holidays. This value is proposed by the system and could be changed by the user |
| 33 | transportDaysProposed | Ημέρες Μετακίνησης Εργασιών (προτεινόμενη τιμή) | number (readonly) | - | - | {icon check} | equals (returnDate - departDate) - Weekends - Holidays. This value is proposed by the system |
| 34 | overnightsNumManual | Διανυκτερεύσεις | number  | - | - | {icon check} | this field represents the sum of overnights proposed by the system and could be changed by the user|
| 35 | overnightsNumProposed | Διανυκτερεύσεις (προτεινόμενη τιμή) | number (readonly) | - | - | {icon check} | this field represents the sum of overnights proposed by the system |
| 36 | compensationDaysManual | Ημέρες Αποζημίωσης | number | - | - | {icon check} | equals (taskEndDate - taskStartDate) + departDate. This value is proposed by the system and could be changed by the user |
| 37 | compensationDaysProposed | Ημέρες Αποζημίωσης (προτεινόμενη τιμή) (readonly) | number | - | - | {icon check} | equals (taskEndDate - taskStartDate) + departDate. This value is proposed by the system |
| 38 | sameDayReturnTask | Αυθημερόν Επιστροφή | boolean | false | check if departDate == returnDate | {icon check} | automatically filled by the system |
| 39 | tripDaysBefore | Εναπομείνασες Ημέρες Μετακίνησης Εργασιών: Πριν | number | 60 | < 60 | {icon check} | trip days assigned to the employee before his transportation |
| 40 | tripDaysAfter | Εναπομ. Ημ. Μετακ. Εργ.: Μετά | number | - | < 60 | {icon check} | trip days remained to the employee after his transportation |
| 41 | overnightsSumCost | Σύνολο Διανυκτέρευσης | number (readonly) | - | - | {icon check} | equals  overnightsNumManual * accommodation |
| 42 | compensationLevel | Αποζημίωση (Ημερήσια) | number (readonly) | - | - | {icon check} | the amount of the daily compensation which is determined by the user's and the country's category (*see table "Daily Compensation" below) |
| 43 | compensationFinal | Σύνολο Ημερήσιας Αποζημίωσης | number (readonly) | - | - | {icon check} | equals compensationDaysManual * compensationLevel |
| 44 | totalCost | ΣΥΝΟΛΟ | number (readonly) | - | - | {icon check} | equals in general compensationFinal + overnightsSumCost + transportation + additionalExpenses + nonGrnetQuota (for more details see below) |

|Daily Compensation|
| Country Category | Α | Β | Γ |
| User Category Ι | 100 € | 80 € | 60 € |
| User Category ΙΙ | 80 € | 60 € | 50 € |

| Daily Compensation - Rules |
| 1 | Η ημερήσια αποζημίωση καταβάλλεται **ολόκληρη** | Για την ημέρα μετάβασης και επιστροφής, όταν αυτή συμπίπτει με τη λήξη εργασιών | για κάθε ημέρα παραμονής και διανυκτέρευσης |
| 2 | Καταβάλλεται **μειωμένη κατά 50%** | η επιστροφή πραγματοποιείται αυθημερόν (sameDayReturnTask == true) | στην περίπτωση που παρέχεται ημιδιατροφή (food == half board) |
| 3 | Καταβάλλεται **μειωμένη κατά 75%** | καλύπτονται τα έξοδα διατροφής και διανυκτέρευσης (food == full board) |
| 4 | Σε περίπτωση κάλυψης μέρους της αποζημίωσης από άλλον φορέα, καταβάλλεται το υπόλοιπο του ποσού που δικαιούται ο μετακινούμενος (compensationFinal = compensationFinal - compensationFinal*nonGrnetQuota ) |

| Petition States | Label | Description | Petition Status Transitions |
| 1 | Σε επεξεργασία από τον μετακινούμενο | when the simple user create or edit a petition |
| 2 | Υποβεβλημένη από τον μετακινούμενο | when the simple user submits a petition |
|   |  |  |  2 --> 1 : the user can cancel the submission of the petition if the secretary haven't edit the petition yet |
| 3 | Σε επεξεργασία από τη γραμματεία | when the secretary saves the petition for the 1st time and until she submit it |
| 4 | Οριστικοποιημένη από τη γραμματεία | when the secretary submits the petition |
| 5 | Απόφαση Μετακίνησης για ανάρτηση στη ΔΙΑΥΓΕΙΑ |
| 6 | Απόφαση Μετακίνησης υπογεγραμμένη από τον Πρόεδρο |
| 7 | Σε επεξεργασία από μετακινούμενο για αποζημίωση |
| 8 | Υποβεβλημένη από τον μετακινούμενο για αποζημίωση |
| 9 | Σε επεξεργασία από τον Υπεύθυνο Μετακινήσεων |
| 10 | Οριστικοποιημένη από τον Υπεύθυνο Μετακινήσεων |
| 11 | Απόφαση Αποζημίωσης για ανάρτηση στη ΔΙΑΥΓΕΙΑ |
| 12 | Απόφαση Αποζημίωσης υπογεγραμμένη από τον Πρόεδρο |
| 13 | Ολοκληρωμένη |
| 14 | Ακυρωμένη |
