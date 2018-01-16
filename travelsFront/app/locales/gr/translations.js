export default {
	errors : {
		description: "Αυτό το πεδίο",
    inclusion: "{{description}} δεν περιέχεται στη λίστα",
    exclusion: "{{description}} υπάρχει ήδη",
    invalid: "{{description}} δεν είναι έγκυρο",
    confirmation: "{{description}} δεν ταιριάζει με: {{on}}",
    accepted: "{{description}} πρέπει να είναι αποδεκτό",
    empty: "{{description}} δεν μπορεί να είναι κενό",
    blank: "{{description}} δεν μπορεί να είναι κενό",
    present: "{{description}} θα πρέπει να είναι κενό",
    collection: "{{description}} θα πρέπει να αποτελεί σύνολο πεδίων",
    singular: "{{description}} δεν μπορεί να αποτελεί σύνολο πεδίων",
    tooLong: "{{description}} είναι πολύ μεγάλο (μέγιστη τιμή: {{max}} χαρακτήρες)",
    tooShort: "{{description}} είναι πολύ μικρό (ελάχιστη τιμή: {{min}} χαρακτήρες)",
    before: "{{description}} θα πρέπει να είναι πριν από: {{before}}",
    after: "{{description}} θα πρέπει να είναι μετά από: {{after}}",
    wrongDateFormat: "{{description}} θα πρέπει να είναι της μορφής: {{format}}",
    wrongLength: "{{description}} έχει λάθος μήκος (θα πρέπει να αποτελείται από {{is}} χαρακτήρες)",
    notANumber: "{{description}} θα πρέπει να είναι αριθμός",
    notAnInteger: "{{description}} θα πρέπει να είναι ακέραιος",
    greaterThan: "{{description}} θα πρέπει να είναι μεγαλύτερο από {{gt}}",
    greaterThanOrEqualTo: "{{description}} θα πρέπει να είναι μεγαλύτερο ή ίσο με {{gte}}",
    equalTo: "{{description}} θα πρέπει να είναι ίσο με {{is}}",
    lessThan: "{{description}} θα πρέπει να είναι μικρότερο από  {{lt}}",
    lessThanOrEqualTo: "{{description}} θα πρέπει να είναι μικρότερο ή ίσο με {{lte}}",
    otherThan: "{{description}} θα πρέπει να είναι διαφορετικό από {{value}}",
    odd: "{{description}} θα πρέπει να είναι περιττός αριθμός",
    even: "{{description}} θα πρέπει να είναι άρτιος αριθμός",
    positive: "{{description}} θα πρέπει να είναι θετικό",
    date: "{{description}} θα πρέπει να είναι μια έγκυρη ημερομηνία",
    email: "{{description}} θα πρέπει να είναι μια έγκυρη διεύθυνση email",
    phone: "{{description}} θα πρέπει να είναι ένας έγκυρος αριθμός τηλεφώνου",
    url: "{{description}} θα πρέπει να είναι ένα έγκυρο url", 
 	},
	//account labels
	'login_pass.label': 'Κωδικός Πρόσβασης',
	'password.label': 'Κωδικός Πρόσβασης',
  //password labels
  'new_password.label': 'Νέος Κωδικός Πρόσβασης', 
  're_new_password.label': 'Επιβεβαίωση νέου Κωδικού Πρόσβασης', 
  'current_password.label': 'Τρέχων Κωδικός Πρόσβασης',
	//profile labels
	'username.label': 'Όνομα Χρήστη (username)',
	'email.label': 'Email',
	'first_name.label': 'Όνομα',
	'last_name.label': 'Επώνυμο',
	'iban.label': 'IBAN',
	'specialty.label': 'Ειδικότητα',
 	'kind.label': 'Ιδιότητα',
 	'tax_reg_num.label': 'ΑΦΜ',
 	'tax_office.label': 'ΔΟΥ',
 	'user_category.label': 'Κατηγορία Χρήστη',
 	'my_account.label': 'Στοιχεία Λογαριασμού',
 	'personal_info.label': 'Προσωπικά Στοιχεία',
  'hint_email.label': 'Μια έγκυρη διεύθυνση email',
 	//petition labels
 	'dse.label': 'ΔΣΕ',
 	'project.label': 'Έργο',
 	'reason.label': 'Αιτιολογία Μετακίνησης',
 	'departure_point.label': 'Τόπος Αναχώρησης - Από:',
 	'arrival_point.label': 'Τόπος Προορισμού - Προς:',
 	'movement_category.label': 'Κατηγορία Μετακίνησης',
 	'country_category.label': 'Κατηγορία Χώρας',
 	'task_start_date.label': 'Έναρξη Εργασιών',
 	'task_end_date.label': 'Λήξη Εργασιών',
 	'depart_date.label': 'Αναχώρηση',
 	'return_date.label': 'Επιστροφή',
 	'means_of_transport.label': 'Μέσο Μετακίνησης',
 	'transportation_cost.label': 'Τιμή Εισιτηρίου',
 	'meals.label': 'Κάλυψη Διατροφής',
  'accommodation_cost.label': 'Διανυκτέρευση (Ημερήσια) - Ευρώ',
 	'accommodation_local_cost.label': 'Διανυκτέρευση (Ημερήσια) - Τοπικό Νόμισμα',
 	'accommodation_local_currency.label': 'Νόμισμα',
 	'additional_expenses_initial.label': 'Λοιπά Έξοδα Μετακίνησης',
  'participation_cost.label': 'Κόστος Συμμετοχής - Ευρώ',
 	'participation_local_cost.label': 'Κόστος Συμμετοχής',
 	'participation_local_currency.label': 'Νόμισμα',
 	'additional_expenses_initial_description.label': 'Λοιπά Έξοδα Μετακίνησης - Περιγραφή',
 	'user_recommendation.label': 'Αρχικές Προτάσεις Μετακινούμενου (για κρατήσεις πτήσεων, ξενοδοχείου, κλπ)',
  'secretary_recommendation.label': 'Στοιχεία σχετικά με την μετακίνηση και τη διαμονή',
  'travel_data.label': 'Στοιχεία μετακίνησης',
  'user_data.label': 'Στοιχεία χρήστη',
  //secretary petition labels
  'timesheets.label': 'Συγχρονισμός με την εφαρμογή Timesheets',
  'timesheeted.label': 'Οι ημέρες μετακίνησης έχουν περαστεί στην εφαρμογή Timesheets',
  'non_grnet_quota.label': 'Κάλυψη ημερήσιας αποζημίωσης από άλλο φορέα',
  'manager_approval.label': 'Έγκριση της Μετακίνησης από τον Υπεύθυνο Έργου',
  'manager_movement_approval.label': 'Έγκριση Αίτησης Μετακίνησης από τον Υπεύθυνο Έργου',
  'manager_cost_approval.label': ' Έγκριση τελικών δαπανών της Μετακίνησης από τον Υπεύθυνο Έργου',
  'secretary_data.label': 'Στοιχεία Αίτησης που καταχωρεί η Γραμματεία',
  'controller_data.label': 'Στοιχεία Αίτησης - Λογιστικός Έλεγχος',
  'computed_data.label': 'Υπολογιζόμενα Οικονομικά Στοιχεία',
  'movement_id.label': 'Αρ.Μετακίνησης',
  'expenditure_date_protocol.label': 'Ημ. Πρ. Αίτησης Δαπάνης Μετακίνησης',
  'expenditure_protocol.label': 'Αρ. Πρ. Αίτησης Δαπάνης Μετακίνησης',
  'movement_date_protocol.label': 'Ημ. Πρ. Απόφασης Μετακίνησης',
  'movement_protocol.label': 'Αρ. Πρ. Απόφασης Μετακίνησης',
  'trip_days_before.label': 'Εναπομείνασες Ημέρες Μετακίνησης Εργασιών: Πριν',
  'transportation_payment_way.label': 'Τρόπος Πληρωμής',
  'transportation_payment_description.label': 'Στοιχεία Πληρωμής',
  'accommodation_payment_way.label': 'Τρόπος Πληρωμής',
  'accommodation_payment_description.label': 'Στοιχεία Πληρωμής',
  'participation_payment_way.label': 'Τρόπος Πληρωμής',
  'participation_payment_description.label': 'Στοιχεία Πληρωμής',
  'travel_info.travel': 'Στοιχεία Μετακίνησης',
  'travel_info.accommodation': 'Στοιχεία Διαμονής',
  'travel_info.transportation': 'Στοιχεία Ταξιδιού',
  'computed_days.label': 'Ημέρες Μετακίνησης',
  //multiple destinations
  'travel_info_number.label': 'Προορισμός #',
  //computational data labels
  'transport_days_manual.label': 'Ημέρες Μετακίνησης Εργασιών',
  'transport_days_proposed.label': 'Ημέρες Μετακίνησης Εργασιών (προτεινόμενη τιμή)',
  'overnights_num_manual.label': 'Διανυκτερεύσεις',
  'overnights_num_proposed.label': 'Διανυκτερεύσεις (προτεινόμενη τιμή)',
  'overnights_proposed.label': 'Διανυκτερεύσεις (προτεινόμενη τιμή)',
  'compensation_days_manual.label': 'Ημέρες Αποζημίωσης',
  'compensation_days_proposed.label': 'Ημέρες Αποζημίωσης (προτεινόμενη τιμή)',
  'same_day_return_task.label': 'Αυθημερόν Επιστροφή',
  'trip_days_before.label': 'Εναπομείνασες Ημέρες Μετακίνησης Εργασιών: Πριν',
  'trip_days_after.label': 'Εναπομ. Ημ. Μετακ. Εργ.: Μετά',
  'overnights_sum_cost.label': 'Σύνολο Διανυκτέρευσης',
  'compensation_level.label': 'Αποζημίωση (Ημερήσια)',
  'compensation_cost.label': 'Σύνολο Ημερήσιας Αποζημίωσης',
  'total_cost_calculated.label': 'ΣΥΝΟΛΟ',
 	//buttons
 	'form.button.save': 'Αποθηκευση',
 	'form.button.submit': 'Υποβολη',
 	'form.button.login': 'Εισοδος',
  'form.button.signup': 'Εγγραφη',
  'file.button.delete': 'Διαγραφη',
  'file.button.download': 'Ληψη',
  'password.button.change': 'Αλλαγη',
  'list.button.search': 'Αναζητηση',
  'list.button.clear': 'Καθαρισμος Φιλτρων',
  'stats.button.export': 'Εξαγωγη',
  'form.button.add_destination': 'Προσθηκη Προορισμου ( + )',
  'form.button.remove_destination': 'Αφαιρεση Προορισμου ( - )',
  //placeholders
  'placeholder.filterByProject': 'Έργο',
  'placeholder.filterByName': 'Επώνυμο',
  'placeholder.filterByStatus': 'Ιστορικό',
  'placeholder.filterByDSE': 'ΔΣΕ',
  'placeholder.filterByStartDateFrom': 'Ημ/νία Αναχώρησης - Από',
  'placeholder.filterByStartDateTo': 'Ημ/νία Αναχώρησης - Έως',
  'placeholder.filterByEndDate': 'Ημ/νία Επιστροφής',
  'placeholder.filterWithdrawn': 'Κατάσταση Αίτησης',
 	//tabs
 	'login.tab': 'Είσοδος',
 	'signup.tab': 'Εγγραφή',
 	'logout.tab': 'Eξοδος',
 	'profile.tab': 'Προφίλ',
  'password.change.tab': 'Αλλαγή Κωδικού Πρόσβασης',
 	'new_petition.tab': 'Νέα Αίτηση',
 	'my_petitions.tab': 'Οι Αιτήσεις μου',
 	'submitted_petitions.tab': 'Υποβεβλημένες Αιτήσεις',
  'help.tab': 'Οδηγίες Χρήσης',
 	'petitions_list.tab': 'Λίστα Αιτήσεων',
  'manager_petitions_list.tab': 'Λίστα Αιτήσεων προς Έγκριση',
  'statistics.tab': 'Εξαγωγή Στατιστικών',
 	//titles
 	'login.title': 'Είσοδος',
 	'logged_in_as.title': 'Συνδεθήκατε ως: ',
 	'signup.title': 'Δημιουργία Λογαριασμού',
 	'profile.title': 'Προφίλ',
  'password_change.title': 'Αλλαγή Κωδικού Πρόσβασης',
 	'petition_create.title': 'Δημιουργία Αίτησης Μετακίνησης',
 	'petition_edit.title': 'Επεξεργασία Αίτησης Μετακίνησης',
  'compensation_edit.title': 'Επεξεργασία Αίτησης Αποζημίωσης',
 	'petition_list.title': 'Λίστα Αιτήσεων',
  'filters.title': 'Φίλτρα Αναζήτησης',
  'statistics.title': 'Εξαγωγή Στατιστικών',
  'stats.title.export': 'Εξαγωγή Στατιστικών με βάση το Έργο',
  'stats.title.full_export': 'Εξαγωγή Γενικών Στατιστικών',
  //travel_report labels
  'travel_report.label': 'Απολογισμός Ταξιδιού',
  'travel_files.label': 'Ανέβασμα Αρχείων (μέγιστο μέγεθος 8MB)',
  'travel_report.label': 'Απολογισμός Μετακίνησης',
  'additional_expenses.label': 'Λοιπά Έξοδα Μετακίνησης',
  'additional_expenses_local_currency.label': 'Νόμισμα',
  'additional_expenses_description.label': 'Λοιπά Έξοδα Μετακίνησης - Περιγραφή',
  'compensation_petition_date.label': 'Ημ. Πρ. Αίτησης Αποζημίωσης Μετακίνησης', 
  'compensation_petition_protocol.label': 'Αρ. Πρ. Αίτησης Αποζημίωσης Μετακίνησης', 
  'compensation_decision_date.label': 'Ημ. Πρ. Απόφασης Αποζημίωσης Μετακίνησης', 
  'compensation_decision_protocol.label': 'Αρ. Πρ. Απόφασης Αποζημίωσης Μετακίνησης',
  //compensation labels
  'additional_expenses_description_user.label': 'Λοιπά Έξοδα Μετακίνησης - Περιγραφή - Καταχώρηση Χρήστη',
  'additional_expenses_user.label': 'Λοιπά Έξοδα Μετακίνησης - Καταχώρηση Χρήστη',
  //tooltips
  'tooltip_edit': 'Επεξεργασία Αίτησης',
  'tooltip_delete': 'Διαγραφή Αίτησης',
  'tooltip_undo': 'Αναίρεση Υποβολής',
  'tooltip_withdraw': 'Ακύρωση Αίτησης',
  'tooltip_withdraw_cancel': 'Επαναφορά Αίτησης',
  'tooltip_approve_undo': 'Αναίρεση Έγκρισης',
  'tooltip_view': 'Επισκόπηση Αίτησης',
  'pdf_travel_application': 'Εξαγωγή Αίτησης Δαπάνης Μετακίνησης',
  'pdf_travel_decision': 'Εξαγωγή Απόφασης Μετακίνησης',
  'pdf_compensation_application': 'Εξαγωγή Αίτησης Αποζημίωσης Μετακίνησης',
  'pdf_compensation_decision': 'Εξαγωγή Απόφασης Αποζημίωσης',
  'travel_presidentApproval': 'Έγκριση Μετακίνησης',
  'compensation_presidentApproval': 'Έγκριση Αποζημίωσης',
  'travel_managerApproval': 'Έγκριση Αίτησης Μετακίνησης',
  'travel_managerCostApproval': 'Έγκριση Δαπάνης Μετακίνησης',
  'del_action_info_message': 'Αφού επιλέξετε την "ΔΙΑΓΡΑΦΗ" του αρχείου, στη συνέχεια πατήστε το κουμπί "ΑΠΟΘΗΚΕΥΣΗ" προκειμένου να πραγματοποιηθεί η ενέργεια της διαγραφής',
  'tooltip_save_b4_submit': 'Για να υποβάλετε την αίτησή σας θα πρέπει πρώτα να αποθηκεύσετε τις αλλαγές σας',
  //prompt messages
  'prompt_delete_title': 'Διαγραφή Αίτησης',
  'prompt_delete_message': 'Είστε βέβαιοι ότι θέλετε να διαγράψετε την αίτηση σας;',
  'prompt_undo_title': 'Αναίρεση Υποβολής',
  'prompt_undo_message': 'Είστε βέβαιοι ότι θέλετε να αναιρέσετε την υποβολή την αίτηση σας;',
  'prompt_submit_title': 'Υποβολή Αίτησης',
  'prompt_submit_message': 'Είστε βέβαιοι ότι θέλετε να υποβάλετε την αίτηση σας;',
  'prompt_withdraw_title': 'Ακύρωση Αίτησης',
  'prompt_withdraw_message': 'Είστε βέβαιοι ότι θέλετε να ακυρώσετε την αίτηση μετακίνησης;',
  'prompt_withdrawCancel_title': 'Επαναφορά Ακυρωμένης Αίτησης',
  'prompt_withdrawCancel_message': 'Είστε βέβαιοι ότι θέλετε να επαναφέρετε την ακυρωμένη αίτηση μετακίνησης;',
  'prompt_limit_title': 'ΠΡΟΣΟΧΗ! Υπέρβαση Ορίου Διανυκτέρευσης',
  'prompt_limit_message': 'Έχετε υπερβεί το όριο της τιμής διανυκτέρευσης που ορίζεται από το νόμο. Εάν είστε βέβαιοι ότι θέλετε να υποβάλετε την αίτηση, επιλέξτε το κουμπί ΟΚ.',
  'prompt_approve_title': 'Έγκριση Αίτησης Μετακίνησης',
  'prompt_approve_message': 'Είστε βέβαιοι ότι θέλετε να εγκρίνετε την αίτηση μετακίνησης;',
  'prompt_cost_approve_title': 'Έγκριση Δαπάνης Μετακίνησης',
  'prompt_cost_approve_message': 'Είστε βέβαιοι ότι θέλετε να εγκρίνετε την δαπάνη μετακίνησης;',
  'prompt_submit_comp_message': 'Είστε βέβαιοι ότι θέλετε να υποβάλετε την αίτηση σας;'+'<br>'+'<br>'
  +'Σημειώνεται ότι πριν την τελική υποβολή θα πρέπει να κατεβάσετε την Αίτηση Δαπάνης Μετακίνησης, μέσω της επιλογής από τη λίστα αιτήσεων.'+'<br>'+'<br>'
  +'Το συγκεκριμένο έγγραφο θα πρέπει να το επισυνάπτετε πάντοτε στον φυσικό φάκελο με τα αποδεικτικά έγγραφα των εξόδων που προσκομίζεται στο Λογιστήριο.',
  'prompt_secretary_submit_message': 'Επισημαίνουμε ότι κατά την υποβολή της αίτησης, οι υπολογισμοί πραγματοποιούνται με βάση τις τιμές των πεδίων:'+'<br>'
  +'(α) Ημέρες Μετακίνησης Εργασιών,'+'<br>'
  +'(β) Διανυκτερεύσεις,'+'<br>'
  +'(γ) Ημέρες Αποζημίωσης',
  'prompt_done_title': 'Έγκριση από Πρόεδρο',
  'prompt_done_message': 'Με τη συγκεκριμένη ενέργεια η αίτηση θα περάσει στην κατάσταση "εγκεκριμένη από Πρόεδρο"',
  //success messages
  'petition_saved': 'Η αίτησή σας έχει αποθηκευτεί επιτυχώς',
  'profile_saved': 'Τα στοιχεία του προφίλ σας έχουν ενημερωθεί επιτυχώς',
  //placeholders
  'time_placeholder': 'Ώρα',
  //select options
  'option.withdrawn': 'Ακυρωμένες Αιτήσεις',
  'option.active': 'Ενεργές Αιτήσεις',
};
