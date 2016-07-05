import datetime




def checkPetitionCompleteness(request, status):
        """TODO: Docstring for checkDataCompleteness.

        :request: TODO
        :returns: TODO

        """
        missing_field = None

        user_groups = request.user.groups.all()
        user_group_name = 'Unknown'
        if user_groups:
            user_group_name = user_groups[0].name
        try:
            name = request.data['name']
            surname = request.data['surname']
            iban = request.data['iban']
            specialtyID = request.data['specialtyID']
            taxRegNum = request.data['taxRegNum']
            taxOffice = request.data['taxOffice']
            kind = request.data['kind']
            taskStartDate = request.data['taskStartDate']
            taskEndDate = request.data['taskEndDate']
            if status > 2:
                depart_date = request.data['depart_date']
                return_date = request.data['return_date']
            project = request.data['project']
            reason = request.data['reason']
            movementCategory = request.data['movementCategory']
            departurePoint = request.data['departurePoint']
            arrivalPoint = request.data['arrivalPoint']
            transportation = request.data['transportation']
        except KeyError:
            print "Shit"
            return [False, missing_field]

        none_mandatory_fields = ['accomondation', 'recCostParticipation',
                                 'recTransport', 'recAccomondation',
                                 'depart_date', 'return_date',
                                 'advanced_info',
                                 'additional_expenses_initial',
                                 'additional_expenses_initial_description']
        if user_group_name in ['SECRETARY', 'Unknown']:
            none_mandatory_fields = ['accomondation', 'recCostParticipation',
                                     'recTransport', 'recAccomondation',
                                     'advanced_info']
        keys = request.data.keys()

        for key in keys:
            if key not in none_mandatory_fields:
                value = request.data[key]
                if value is None or value == '':
                    missing_field = key
                    return [False, missing_field]
            else:
                continue

        return [True, missing_field]


def checkAdvancedPetitionCompleteness(advanced_petition):

        none_mandatory_fields = ['compensation_petition_protocol',
                                 'compensation_petition_date',
                                 'compensation_decision_protocol',
                                 'compensation_decision_date']
        ap_missing_field = None

        for f in advanced_petition._meta.get_fields():
            field_name = f.name
            field_value = getattr(advanced_petition, field_name)
            print str(field_name) + ",value:" + str(field_value)
            if (field_value is None or field_value == '')\
                    and field_name not in none_mandatory_fields:
                ap_missing_field = field_name
                return [False, ap_missing_field]

        return [True, ap_missing_field]


def date_check(task_start, task_end, depart_date, return_date,
               user_group, status):

        result = {'error': False, 'msg': ''}
        now = datetime.datetime.now()

        task_start = datetime.datetime.strptime(
            task_start, '%Y-%m-%dT%H:%M')

        task_end = datetime.datetime.strptime(
            task_end, '%Y-%m-%dT%H:%M')

        if task_start < now:
            result['error'] = True
            result['msg'] = 'Task start date should be after today'
            return result

        if task_end < now:

            result['error'] = True
            result['msg'] = 'Task end date should be after today'
            return result

        if task_end < task_start:

            result['error'] = True
            result['msg'] = 'Task end date should be after task start date'
            return result

        if user_group in ['SECRETARY', 'Unknown'] and status > 2:
            depart_date = datetime.datetime.strptime(
                depart_date, '%Y-%m-%dT%H:%M')

            return_date = datetime.datetime.strptime(
                return_date, '%Y-%m-%dT%H:%M')
            if depart_date < now:
                result['error'] = True
                result['msg'] = 'Depart date should be after today'
                return result

            if return_date < now:
                result['error'] = True
                result['msg'] = 'Return date should be after today'
                return result

            if return_date < depart_date:

                result['error'] = True
                result['msg'] = 'Return date should be after departure date'
                return result
        return result
