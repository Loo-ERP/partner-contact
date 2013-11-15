# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2009 Tiny SPRL (<http://tiny.be>).
#    Copyright (C) 2013 initOS GmbH & Co. KG (<http://www.initos.com>).
#    Author Thomas Rehn <thomas.rehn at initos.com>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from openerp.osv import orm, fields


class ResPartner(orm.Model):
    """Assigns 'ref' from a sequence on creation and copying"""

    _inherit = 'res.partner'

    def create(self, cr, uid, vals, context=None):
        context = context or {}
        if not vals.get('ref') and self._needsRef(cr, uid, vals=vals, context=context):
            vals['ref'] = self.pool.get('ir.sequence').get(cr, uid, 'res.partner')
        return super(ResPartner, self).create(cr, uid, vals, context)

    def copy(self, cr, uid, id, default=None, context=None):
        default = default or {}
        if not default.get('ref') and self._needsRef(cr, uid, id=id, context=context):
            default['ref'] = self.pool.get('ir.sequence').get(cr, uid, 'res.partner', context=context)
        return super(ResPartner, self).copy(cr, uid, id, default, context=context)

    def _needsRef(self, cr, uid, id=None, vals=None, context=None):
        """
        Checks whether a sequence value should be assigned to a partner's 'ref'

        :param cr: database cursor
        :param uid: current user id
        :param id: id of the partner object
        :param vals: known field values of the partner object
        :return: true iff a sequence value should be assigned to the partner's 'ref'
        """
        if not vals and not id:
            raise Exception('Either field values or an id must be provided.')
        # only assign a 'ref' if it is a customer or supplier and 
        # if it not a child object (such as a shipping/invoice address)
        if id:
            vals = self.read(cr, uid, id, ['parent_id','customer','supplier'], context=context)
        return not vals.get('parent_id') and (vals.get('customer') or vals.get('supplier'))

    _columns = {
        'ref': fields.char('Reference', size=64, readonly=True),
    }

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
