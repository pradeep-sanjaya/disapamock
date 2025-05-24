from flask import Flask, jsonify, request

app = Flask(__name__)

# In-memory storage
users_payment_methods = {
    "1": {
        "creditcard": [
            {
                "id": "c073669a-4ee7-49c1-8a3d-924bc19d8ee9",
                "maskedCard": "**** **** **** 8765",
                "isDefault": True,
                "expiryDate": "12/25"
            },
            {
                "id": "d183669a-4ee7-49c1-8a3d-924bc19d8ee0",
                "maskedCard": "**** **** **** 1234",
                "isDefault": False,
                "expiryDate": "06/24"
            }
        ],
        "mpesa": [
            {
                "id": "b173669a-1aa7-49c1-8a3d-924bc19d8ee9",
                "walletId": "7740331230",
                "isDefault": True
            }
        ]
    }
}

@app.route('/api/users/<string:user_id>/payment-methods', methods=['GET'])
def get_payment_methods(user_id):
    """Get all payment methods for a user"""
    if user_id not in users_payment_methods:
        return jsonify({
            "success": False,
            "message": "User not found",
            "data": None
        }), 404
        
    return jsonify({
        "success": True,
        "message": "Operation successful",
        "data": users_payment_methods[user_id]
    })

@app.route('/api/users/<string:user_id>/payment-methods/default', methods=['GET'])
def get_default_payment_method(user_id):
    """Get default payment method for a user"""
    if user_id not in users_payment_methods:
        return jsonify({
            "success": False,
            "message": "User not found",
            "data": None
        }), 404
    
    # Find the default payment method
    for method_type, methods in users_payment_methods[user_id].items():
        for method in methods:
            if method.get('isDefault', False):
                response_data = {
                    "type": method_type,
                    "id": method["id"]
                }
                if method_type == 'creditcard':
                    response_data["details"] = {
                        "maskedCard": method["maskedCard"],
                        "expiryDate": method["expiryDate"]
                    }
                else:  # mpesa
                    response_data["details"] = {
                        "walletId": method["walletId"]
                    }
                
                return jsonify({
                    "success": True,
                    "message": "Default payment method retrieved successfully",
                    "data": response_data
                })
    
    return jsonify({
        "success": True,
        "message": "No default payment method found",
        "data": None
    })

@app.route('/api/users/<string:user_id>/payment-methods/default', methods=['PATCH'])
def set_default_payment_method(user_id):
    """Set default payment method for a user"""
    if user_id not in users_payment_methods:
        return jsonify({
            "success": False,
            "message": "User not found",
            "data": None
        }), 404
    
    data = request.get_json()
    method_type = data.get('type')
    method_id = data.get('id')
    
    if not method_type or not method_id:
        return jsonify({
            "success": False,
            "message": "type and id are required",
            "data": None
        }), 400
    
    if method_type not in users_payment_methods[user_id]:
        return jsonify({
            "success": False,
            "message": f"Invalid payment method type: {method_type}",
            "data": None
        }), 400
    
    # Find the method to set as default
    method_found = False
    for method in users_payment_methods[user_id][method_type]:
        if method['id'] == method_id:
            method_found = True
            # Set all methods of this type to not default
            for m in users_payment_methods[user_id][method_type]:
                m['isDefault'] = False
            # Set this method as default
            method['isDefault'] = True
            break
    
    if not method_found:
        return jsonify({
            "success": False,
            "message": f"Payment method with id {method_id} not found",
            "data": None
        }), 404
    
    return jsonify({
        "success": True,
        "message": f"Default {method_type} payment method updated successfully",
        "data": None
    })

@app.route('/api/users/<string:user_id>/payment-methods/<string:method_id>', methods=['DELETE'])
def delete_payment_method(user_id, method_id):
    """Delete a payment method"""
    if user_id not in users_payment_methods:
        return jsonify({
            "success": False,
            "message": "User not found",
            "data": None
        }), 404
    
    method_found = False
    method_type = None
    
    # Find and remove the method
    for m_type, methods in users_payment_methods[user_id].items():
        for i, method in enumerate(methods):
            if method['id'] == method_id:
                method_found = True
                method_type = m_type
                # Don't allow deleting the last payment method
                if len(methods) == 1 and len(users_payment_methods[user_id]) == 1:
                    return jsonify({
                        "success": False,
                        "message": "Cannot delete the last payment method",
                        "data": None
                    }), 400
                
                # If deleting default, set another method as default
                if method.get('isDefault', False) and len(methods) > 1:
                    # Find another method to set as default
                    for other_method in methods:
                        if other_method['id'] != method_id:
                            other_method['isDefault'] = True
                            break
                
                # Remove the method
                users_payment_methods[user_id][m_type].pop(i)
                break
        if method_found:
            break
    
    if not method_found:
        return jsonify({
            "success": False,
            "message": f"Payment method with id {method_id} not found",
            "data": None
        }), 404
    
    return jsonify({
        "success": True,
        "message": f"{method_type} payment method deleted successfully",
        "data": None
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)
