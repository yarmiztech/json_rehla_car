import requests
from odoo import http
from odoo.http import request
import json
import decimal
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT,DEFAULT_SERVER_DATETIME_FORMAT


import werkzeug.urls
import werkzeug.utils
from werkzeug.exceptions import BadRequest
# import yaml
import time
from datetime import datetime

from odoo import http
from odoo.addons.sale.controllers.onboarding import OnboardingController



class Trackmenu(http.Controller):

    @http.route('/Saleorders', auth='public', methods=['GET'])
    def salesorders(self, **kw):
        cargo_status_list = http.request.env['sale.order'].sudo().search(
            [])[0]
        products_list = []
        for cargo_status in cargo_status_list.order_line:
            products_list.append({
                'Reference Id': '1',
                'Partner Name': cargo_status.order_id.partner_id.name,
                'mobile': cargo_status_list[0].partner_id.mobile or None,
                'state': cargo_status.order_id.state,
                'Product Name': cargo_status.product_id.name,
                'Product Quantity': cargo_status.product_uom_qty,
                'Price': cargo_status.price_unit,
                'Driver': 'Driver Name',
                'Driver Mobile': '999999999',
                'Purchase Product': cargo_status.product_id.name,
                'Purchase Price': '1000'
            })
        data = products_list
        print(data)
        print(json.dumps(data))

        # return json.dumps({cargo_status})
        def dec_serializer(self):
            if isinstance(self, decimal.Decimal):
                return float(self)

        return json.dumps(data, default=dec_serializer(self))

    @http.route('/Saleorders/Cancel', auth='public', methods=['GET'])
    def salesorders_cancel(self, **kw):
        cargo_status_list = http.request.env['sale.order'].sudo().search(
            [])[0]
        products_list = []
        for cargo_status in cargo_status_list.order_line:
            products_list.append({
                'Reference Id': '1',
                'Partner Name': cargo_status.order_id.partner_id.name,
                'mobile': cargo_status_list[0].partner_id.mobile or None,
                'state': 'Cancel',
                'Driver': 'Driver Name',
                'Driver Mobile': '999999999',
            })
        data = products_list
        print(data)
        print(json.dumps(data))

        # return json.dumps({cargo_status})
        def dec_serializer(self):
            if isinstance(self, decimal.Decimal):
                return float(self)

        return json.dumps(data, default=dec_serializer(self))

    @http.route('/Trip/LastId', auth='public', methods=['GET'])
    def salesorders_last(self, **kw):
        cargo_status_list = http.request.env['sale.order'].sudo().search(
            [])[0]
        products_list = []
        for cargo_status in cargo_status_list:
            products_list.append({
                'Last TripId': cargo_status.trip_id,
                'Last Id': cargo_status.rehla_id,
                'Passenger Name': cargo_status.partner_id.name,
                'Date':cargo_status.create_date.isoformat(),

            })
        data = products_list
        print(data)
        print(json.dumps(data))

        # return json.dumps({cargo_status})
        def dec_serializer(self):
            if isinstance(self, decimal.Decimal):
                return float(self)

        return json.dumps(data, default=dec_serializer(self))

    @http.route('/Saleorders/payment', auth='public', methods=['GET'])
    def salesorders_payment(self, **kw):
        products_list = []
        products_list.append({
            'Reference Id': '1',
            'Partner Name': 'Partner Name',
            'mobile': 'Partner Mobile Number',
            'Payment Amount': '1000',
            'Payment Journal': 'Cash or Bank',
            'state': 'draft or posted'
        })
        data = products_list
        print(data)
        print(json.dumps(data))

        # return json.dumps({cargo_status})
        def dec_serializer(self):
            if isinstance(self, decimal.Decimal):
                return float(self)

        return json.dumps(data, default=dec_serializer(self))

    @http.route('/Saleorders/payment/cancel', auth='public', methods=['GET'])
    def salesorders_payment_cancel(self, **kw):
        products_list = []
        products_list.append({
            'Reference Id': '1',
            'Partner Name': 'Partner Name',
            'mobile': 'Partner Mobile Number',
            'Payment Amount': '1000',
            'Payment Journal': 'Cash or Bank',
            'state': 'Cancel'
        })
        data = products_list
        print(data)
        print(json.dumps(data))

        # return json.dumps({cargo_status})
        def dec_serializer(self):
            if isinstance(self, decimal.Decimal):
                return float(self)

        return json.dumps(data, default=dec_serializer(self))

    @http.route('/Create_Orders', auth='public', methods=['GET'])
    def estimate_create_orders(self, **rec):
        # http.request.env['ir.config_parameter'].get_param('web.base.url')
        responce = requests.get("http://rehlaapi.native-tech.co/api/GetTripsReportForERP")
        # responce = requests.get("http://5.189.161.117:8069/Estimate/Orders?id=1")
        # line_data = json.loads(rec['data'])
        # current_u = http.request.env['ir.config_parameter'].get_param('web.base.url') + http.request.httprequest.full_path
        # responce = requests.get(request.httprequest.__dict__['url'])
        if responce:
            line_data = json.loads(responce.text)
            # line_data = line_data['model']
            if line_data['model'][0]['Reservations'][0]:
                if not request.env['sale.order'].sudo().search([('trip_id','=',line_data['model'][0]['Reservations'][0]['TripId'])]):
                    partner_id = request.env['res.partner'].sudo().search(
                        [('passenger_id', '=', line_data['model'][0]['Reservations'][0]['PassengerId'])])
                    if not partner_id:
                        partner_id = request.env['res.partner'].sudo().create({
                            'name': line_data['model'][0]['Reservations'][0]['PassengerName'],
                            'passenger_id': line_data['model'][0]['Reservations'][0]['PassengerId'],
                        })

                    product_line = []
                    line = (0, 0, {
                        'product_id': request.env['product.product'].sudo().search([('name', '=', 'Rehla Car')]).id,
                        'product_qty': line_data['model'][0]['Reservations'][0]['SeatCount'],
                        'price_unit': line_data['model'][0]['Reservations'][0]['SeatsCost'],
                        'name': request.env['product.product'].sudo().search([('name', '=', 'Rehla Car')]).name,
                        # 'tax_id':47,
                        'product_uom': (request.env['uom.uom'].sudo().search([('name', '=', 'Units')])).id,

                    })
                    product_line.append(line)

                    vals = {
                        'partner_id': partner_id.id,
                        'trip_id': line_data['model'][0]['Reservations'][0]['TripId'],
                        'rehla_id': line_data['model'][0]['Reservations'][0]['Id'],
                        'order_line': product_line,
                    }
                    order = request.env['sale.order'].sudo().create(vals)
                    return




class CustomOnboardingController(OnboardingController):  # Inherit in your custom class

        @http.route('/sales/sale_quotation_onboarding_panel', auth='user', type='json')
        def sale_quotation_onboarding(self):
            res = super(CustomOnboardingController, self).sale_quotation_onboarding()
            if request.env['sale.order'].sudo().search([]):
                last_trip = request.env['sale.order'].sudo().search([])[0].trip_id
                print(last_trip,'last_trip')
                "https: // apiv2.rehlacar.com / api / GetTripsReportForERP?LastTripId =%s" % last_trip
                responce = requests.get("https://apiv2.rehlacar.com/api/GetTripsReportForERP?LastTripId=%s"%last_trip)
            else:
                 responce = requests.get("https://apiv2.rehlacar.com/api/GetTripsReportForERP?LastTripId=78940")
            # responce = requests.get("http://rehlaapi.native-tech.co/api/GetTripsReportForERP")
           ####################################3
            # responce = requests.get("http://5.189.161.117:8069/Estimate/Orders?id=1")
            # line_data = json.loads(rec['data'])
            # current_u = http.request.env['ir.config_parameter'].get_param('web.base.url') + http.request.httprequest.full_path
            # responce = requests.get(request.httprequest.__dict__['url'])
            if responce:
                line_data = json.loads(responce.text)
                # line_data = line_data['model']
                order = request.env['sale.order']
                i=0
                for each in line_data['model']:
                        print(each['TripCost'],'Trip')
                    # if each['TripCost'] != '78941':
                    # i=i+1
                    # if i <= 10:
                        if each['DriverId']:
                            if not request.env['res.partner'].sudo().search([('reh_driver_id','=',each['DriverId'])]):
                                driver_id = request.env['res.partner'].sudo().create({
                                    'name': each['DriverName'],
                                    'reh_driver_id': each['DriverId'],
                                    'mobile': each['DriverPhoneNumber'],
                                    'email': each['DriverEmail'],
                                    # 'supplier':True

                                })
                            else:
                                driver_id = request.env['res.partner'].sudo().search([('reh_driver_id','=',each['DriverId'])])

                        if driver_id:
                            if not request.env['purchase.order'].sudo().search([('trip_id','=',each['TripId'])]):
                                product_p_line = []

                                # tax_ids = request.env['account.tax'].search([('name', '=', 'VAT 15%'),('type_tax_use','=','purchase')])
                                # tax_ids += request.env['account.tax'].search([('name', '=', 'Percentage 7%'),('type_tax_use','=','purchase')])

                                excluded_value = 0
                                basic_value = 0
                                price_unit=0

                                transportation_aut = each['TransportAuthorityFee']
                                airport_additional = each['AirportAdditionalFees']
                                distance_amount = each['Distance'] * each['KMPrice']
                                print(each['TripId'])
                                actual = distance_amount + each['CaptainPounce'] + each['TransportAuthorityFee'] + each[
                                    'AirportAdditionalFees'] + each['MinimumPay']
                                #52.5###
                                tax_value_system = actual * 7 / 100
                                # 3.67####
                                application_fee = tax_value_system
                                coupon_value = each['CouponValue']
                                actual_cali = actual + tax_value_system - each['CouponValue']
                                value_added =  actual_cali * 15/100


                                trip_cost = each['TripCost']- each['CouponValue']
                                captain_cost = trip_cost - transportation_aut - airport_additional - tax_value_system + coupon_value - value_added
                                price_unit=captain_cost



                                # if tax_ids:
                                #     tax = 0
                                #     for eachs in tax_ids:
                                #         if eachs.children_tax_ids:
                                #             for ch in eachs.children_tax_ids:
                                #                 tax += ch.amount
                                #         else:
                                #             tax += eachs.amount
                                #     value = tax
                                #     # basic_value = each['DriverRevenue'] * value / 100
                                #     # basic_value1 = each['DriverRevenue'] - basic_value
                                #     #
                                #     # # line.basic_value = basic_value
                                #     # # line.basic_value = basic_value
                                #     #
                                #     # # line.total_amount = line.quantity * line.amount
                                #     # excluded_value = 1 * basic_value1
                                #
                                #     value = 100 + tax
                                #     value = value
                                #     basic_value = each['TripCost'] * 100 / value
                                #     price_unit = basic_value / 1
                                print(request.env['product.product'].sudo().search(
                                        [('name', '=', 'Driver Expense')]).id,'product')

                                print(request.env['uom.uom'].sudo().search([('name', '=', 'Units')]),'UOMs')


                                # line = (0, 0, {
                                #     'product_id': request.env['product.product'].sudo().search(
                                #         [('name', '=', 'Driver Expense')]).id,
                                #     'product_qty': 1,
                                #     'product_uom_qty': 1,
                                #     'date_planned': datetime.now().date().strftime(DEFAULT_SERVER_DATE_FORMAT),
                                #     # 'price_unit':each['DriverRevenue'],
                                #     # 'price_unit':excluded_value,
                                #     'price_unit':price_unit,
                                #     'basic_value': basic_value,
                                #     'trip_cost': each['DriverRevenue'],
                                #     'display_type' :'line_section',
                                #     # 'taxes_id':[(6, 0, tax_ids.ids)],
                                #     'name': request.env['product.product'].sudo().search([('name', '=', 'Driver Expense')]).name,
                                #     'product_uom': (request.env['uom.uom'].sudo().search([('name', '=', 'Units')])).id,
                                #
                                # })
                                #
                                #
                                # product_p_line.append(line)

                                po = request.env['purchase.order'].sudo().create({
                                    'partner_id':driver_id.id,
                                    'trip_id':each['TripId'],
                                    'transportation_aut':-transportation_aut,
                                    'airport_additional':-airport_additional,
                                    'taxvalue_system':-tax_value_system,
                                    'value_added':-value_added,
                                    'application_fee':-application_fee,
                                    'coupon_value':+coupon_value,
                                    # 'reh_driver_id':driver_id.reh_driver_id,
                                    'mobile': each['DriverPhoneNumber'],

                                    # 'rehla_id': each['Reservations'][0]['Id'],
                                    # 'order_line':product_p_line,
                                    'order_line':[(0, 0, {
                                                                # 'name': request.env['product.product'].sudo().search([('name', '=', 'Dr0iver Expense')]).name,
                                                                'name': request.env['product.product'].sudo().search([('name', '=', 'Driver Expense')]).name,
                                                                'product_id': request.env['product.product'].sudo().search([('name', '=', 'Driver Expense')]).id,
                                                                'product_qty': 1,
                                                                'product_uom': request.env['uom.uom'].sudo().search([('name', '=', 'Units')]).id,
                                                                'price_unit':price_unit,
                                                                'basic_value': basic_value,
                                                                'trip_cost': each['DriverRevenue'],
                                                                # 'date_planned': time.strftime('%Y-%m-%d'),
                                                                'date_planned': datetime.now().date().strftime(DEFAULT_SERVER_DATE_FORMAT),
                                                            })],
                                })
                                po.sudo().button_confirm()

                                j = request.env['account.payment.method'].sudo().search([('name', '=', 'Manual')])[0]
                                journal = request.env['account.journal'].sudo().search(
                                    [('name', '=', 'Cash'), ('company_id', '=', 1)])

                                if po.amount_total > 0:
                                    inb = po.sudo().automatic_bill_creation()
                                    inb = po.invoice_ids
                                    # inb.sudo().action_invoice_open()
                                    # inb.sudo().action_invoice_open()
                                    # for line in po.invoice_ids.invoice_line_ids:
                                    #     line.basic_value = basic_value
                                        # line.trip_cost = each['DriverRevenue']
                                    if each['Reservations'][0]['PaymentType'] == True :
                                        inb.action_post()
                                        payment = request.env['account.payment'].sudo().create(
                                            {'partner_id': driver_id.id,
                                             'amount': po.amount_total,
                                             'payment_type': 'outbound',
                                             'payment_method_id': request.env.ref(
                                                 'account.account_payment_method_manual_in').id,
                                             'journal_id': journal.id,
                                             'partner_type': 'supplier',
                                             # 'currency_id': self.currency_usd_id,
                                             'ref': po.name+'=>'+driver_id.name,
                                             # 'move_id': inb.id

                                             })

                                        m = payment.sudo().action_post()
                                        # inb.action_post()

                        order = request.env['sale.order']
                        if each['Reservations']:
                            if not request.env['sale.order'].sudo().search(
                                    [('trip_id', '=', each['Reservations'][0]['TripId'])]):
                                partner_id = request.env['res.partner'].sudo().search(
                                    [('passenger_id', '=', each['Reservations'][0]['PassengerId'])])
                                if not partner_id:
                                    partner_id = request.env['res.partner'].sudo().create({
                                        'name': each['Reservations'][0]['PassengerName'],
                                        'passenger_id': each['Reservations'][0]['PassengerId'],
                                        'mobile': each['Reservations'][0]['PassengerPhoneNumber'],
                                        'email': each['Reservations'][0]['PassengerEmail']

                                    })
                                tax_ids = request.env['account.tax'].search(
                                    [('name', '=', 'VAT 15%'), ('type_tax_use', '=', 'sale')])
                                # tax_ids += request.env['account.tax'].search(
                                #     [('name', '=', 'Percentage 7%'), ('type_tax_use', '=', 'sale')])
                                excluded_value=0
                                actual=0
                                # each['Distance']
                                # each['KMPrice']
                                # each['CaptainPounce']
                                # each['TransportAuthorityFee']
                                # each['AirportAdditionalFees']
                                # each['MinimumPay']
                                # each['CouponValue']
                                distance_amount =  each['Distance'] * each['KMPrice']
                                actual = distance_amount+each['CaptainPounce']+ each['TransportAuthorityFee']+each['AirportAdditionalFees']+each['MinimumPay']
                                tax_value_system = actual * 7/100
                                applicable_for = tax_value_system+actual-each['CouponValue']




                                basic_value = 0
                                price_unit =0
                                if tax_ids:
                                    tax = 0
                                    for eachs in tax_ids:
                                        if eachs.children_tax_ids:
                                            for ch in eachs.children_tax_ids:
                                                tax += ch.amount
                                        else:
                                            tax += eachs.amount
                                    value = tax
                                    # basic_value = each['TripCost'] * value / 100
                                    # basic_value = each['TripCost'] * 100 / value
                                    # basic_value1 = each['TripCost'] - basic_value
                                    # line.basic_value = basic_value
                                    # line.basic_value = basic_value

                                    # line.total_amount = line.quantity * line.amount

                                    # value = tax
                                    # basic_value = applicable_for * value / 100
                                    price_unit =applicable_for

                                    # excluded_value = 1 * basic_value1

                                product_line = []
                                line = (0, 0, {
                                    'product_id': request.env['product.product'].sudo().search([('name', '=', 'Rehla Car')]).id,
                                    'product_uom_qty': each['Reservations'][0]['SeatCount'],
                                    # 'price_unit': each['Reservations'][0]['SeatsCost'],
                                    # 'price_unit': each['TripCost'],
                                    'basic_value':basic_value,
                                    'trip_cost':each['TripCost'],
                                    # 'price_unit': excluded_value,
                                    'price_unit': price_unit,
                                    'name': request.env['product.product'].sudo().search([('name', '=', 'Rehla Car')]).name,
                                    'tax_id':[(6,0,tax_ids.ids)],
                                    'product_uom': (request.env['uom.uom'].sudo().search([('name', '=', 'Units')])).id,

                                })
                                product_line.append(line)

                                vals = {
                                    'partner_id': partner_id.id,
                                    'car_categ':str(each['CarCategoryId']),
                                    'trip_id': each['Reservations'][0]['TripId'],
                                    'rehla_id': each['Reservations'][0]['Id'],
                                    'payment_type':str(each['Reservations'][0]['PaymentType']),
                                    'govt_char': each['TransportAuthorityFee'],
                                    'additional_airport': each['AirportAdditionalFees'],
                                    'status_of_trip': str(each['Reservations'][0]['StatusId']),
                                    'order_line': product_line,
                                    'mobile':each['Reservations'][0]['PassengerPhoneNumber'],
                                    'distance':each['Distance'],
                                    'per_km':each['KMPrice'],
                                    'bonus':each['CaptainPounce'],
                                    'transportation_aut':each['TransportAuthorityFee'],
                                    'airport_additional':each['AirportAdditionalFees'],
                                    'taxvalue_system':tax_value_system,
                                    'coupon_value': each['CouponValue'],
                                    'basic_fire':each['MinimumPay'],
                                }
                                order = request.env['sale.order'].sudo().create(vals)
                                order.sudo().action_confirm()
                                if order.status_of_trip != '4':
                                    # invoice = order.action_invoice_create()
                                    invoice = order._create_invoices()
                                    # inb = request.env['account.move'].sudo().browse(invoice[0])
                                    inb = invoice
                                    # inb.sudo().action_invoice_open()
                                    # inb.sudo().action_invoice_open()
                                    for line in inb.invoice_line_ids:
                                        line.basic_value = basic_value
                                        line.trip_cost = each['TripCost']
                                    inb.sudo().action_post()
                                    journal = request.env['account.journal'].sudo().search(
                                        [('name', '=', 'Cash'), ('company_id', '=', 1)])

                                    payment = request.env['account.payment'].sudo().create(
                                        {'partner_id': order.partner_id.id,
                                         'amount': order.amount_total,
                                         'payment_type': 'inbound',
                                         'payment_method_id': request.env.ref(
                                             'account.account_payment_method_manual_in').id,
                                         'journal_id': journal.id,
                                         'partner_type': 'customer',
                                         # 'currency_id': self.currency_usd_id,
                                         'ref': order.name + '=>' + order.partner_id.name,
                                         # 'move_id': inb.id

                                         })
                                    payment.sudo().action_post()
                                    if order:
                                        driv = each['DriverRevenue'] + each['VATValue']
                                        request.env['profit.car.orders'].sudo().create({
                                            'date':datetime.today().date(),
                                            'passenger_id':order.partner_id.passenger_id,
                                            'trip_id': each['Reservations'][0]['TripId'],
                                            'rehla_id': each['Reservations'][0]['Id'],
                                            'reh_driver_id':driver_id.reh_driver_id,
                                            'driver_cost':each['DriverRevenue'],
                                            'trip_cost':each['TripCost'],
                                            'tax_amount':each['VATValue'],
                                            'profit':each['TripCost'] - driv,
                                            'passenger':order.partner_id.id,
                                            'driver':driver_id.id,
                                            'revenue_profit':each['TaxValueAndSystemRevenue']
                                        })
                                        percentage = 0
                                        wallet_amount = 0
                                        if each['Reservations'][0]['PaymentType'] == True:

                                            percentage = each['TripCost'] * 22 / 100
                                            wallet_amount = each['TripCost']-percentage
                                        if each['Reservations'][0]['PaymentType'] == False:

                                            # percentage = each['TripCost'] * 22 / 100
                                            wallet_amount = each['TripCost']

                                        request.env['wallet.amount'].sudo().create({
                                            'date': datetime.today().date(),
                                            'passenger_id': order.partner_id.id,
                                            'trip_id': each['Reservations'][0]['TripId'],
                                            'rehla_id': each['Reservations'][0]['Id'],
                                            'reh_driver_id': driver_id.reh_driver_id,
                                            'driver_cost': each['DriverRevenue'],
                                            'trip_cost': each['TripCost'],
                                            'driver_id':driver_id.id,
                                            'passenger':order.partner_id.id,
                                            'payment_type': str(each['Reservations'][0]['PaymentType']),
                                            'wallet_amount':wallet_amount
                                        })
                                        vals = {
                                            'journal_id': request.env['account.journal'].search(
                                                [('name', '=', 'Miscellaneous Operations'),
                                                 ('company_id', '=', 1)]).id,
                                            'state': 'draft',
                                            'ref': driver_id.name
                                        }
                                        pay_id_list = []
                                        move_id = request.env['account.move'].create(vals)
                                        partner_id = driver_id.id
                                        label = driver_id.name

                                        # if self.type_of_credit == False:
                                        temp = (0, 0, {
                                            'account_id': request.env['account.account'].sudo().search(
                                                [('name', '=', 'Creditors'),
                                                 ('company_id', '=', 1)]).id,
                                            'name': label,
                                            'move_id': move_id.id,
                                            'date': datetime.today().date(),
                                            'partner_id': driver_id.id,
                                            'debit':wallet_amount ,
                                            'credit': 0,
                                        })
                                        pay_id_list.append(temp)

                                        acc = request.env['account.account'].sudo().search(
                                            [('name', '=', 'Cash'),
                                             ('company_id', '=', 1)])
                                        temp = (0, 0, {
                                            'account_id': acc.id,
                                            'name': label,
                                            'move_id': move_id.id,
                                            'date': datetime.today().date(),
                                            'partner_id': driver_id.id,
                                            'debit': 0,
                                            'credit':wallet_amount,
                                        })
                                        pay_id_list.append(temp)
                                        move_id.line_ids = pay_id_list
                                        move_id.sudo().action_post()


                                else:
                                    order.sudo().action_cancel()

            return res