from flask import Flask, render_template, request
from regula_falsi import regula_falsi
from safe_eval import safe_eval_function

app = Flask(__name__)

def generate_step_by_step(f, a, b, iterations_data, tolerance_percent):
    """Generate detailed step-by-step solution from iteration data"""
    step_by_step = {
        'fa_calc': f"{f(a):.6f}",
        'fb_calc': f"{f(b):.6f}",
        'sign_check': f"{(f(a) * f(b)):.6f}",
        'iterations': []
    }
    
    c_prev = None
    for it in iterations_data:
        # Get values from iteration
        current_a = it['a']
        current_b = it['b']
        current_fa = it['fa']
        current_fb = it['fb']
        current_c = it['xr']
        current_fc = it['fxr']
        
        iter_data = {
            'num': it['iteration'],
            'a': current_a,
            'b': current_b,
            'fa': current_fa,
            'fb': current_fb,
            'c': current_c,
            'fc': current_fc,
            'fc_calc': f"f({current_c:.6f})",
        }
        
        # Calculate the formula steps
        numerator = (current_a * current_fb - current_b * current_fa)
        denominator = (current_fb - current_fa)
        iter_data['formula_numerator'] = numerator
        iter_data['formula_denominator'] = denominator
        iter_data['formula_a_times_fb'] = current_a * current_fb
        iter_data['formula_b_times_fa'] = current_b * current_fa
        
        # Add error if available
        if it.get('error') is not None and it['error'] is not None:
            iter_data['error'] = it['error']
            if c_prev is not None:
                iter_data['c_prev'] = c_prev
        
        # Determine update message (FIXED: use update_message instead of update)
        if current_fa * current_fc < 0:
            iter_data['update_message'] = f"Since f(a) · f(c) < 0, the root is between a and c. Update: b = c = {current_c:.6f}"
        else:
            iter_data['update_message'] = f"Since f(a) · f(c) > 0, the root is between c and b. Update: a = c = {current_c:.6f}"
        
        # Check if converged
        if it.get('error') is not None and it['error'] is not None and it['error'] < tolerance_percent:
            iter_data['converged'] = True
        
        step_by_step['iterations'].append(iter_data)
        c_prev = current_c
    
    return step_by_step

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/examples')
def examples():
    return render_template('examples.html')

@app.route('/calculator', methods=['GET', 'POST'])
def calculator():
    result = None
    error = None
    iterations_table = None
    step_by_step = None
    tolerance_percent = None
    
    form_data = {
        'function': 'x**3 - x - 2',
        'a': '1',
        'b': '2',
        'max_iter': '50',
        'tolerance': '1e-6'
    }
    
    if request.method == 'POST':
        try:
            func_str = request.form.get('function', '')
            a = float(request.form.get('a', 0))
            b = float(request.form.get('b', 1))
            max_iter = int(request.form.get('max_iter', 50))
            tolerance = float(request.form.get('tolerance', 1e-6))
            
            tolerance_percent = tolerance
            
            form_data = {
                'function': func_str,
                'a': str(a),
                'b': str(b),
                'max_iter': str(max_iter),
                'tolerance': str(tolerance)
            }
            
            def f(x):
                return safe_eval_function(func_str, x)
            
            fa = f(a)
            fb = f(b)
            
            if fa * fb >= 0:
                error = f"Error: f({a}) = {fa} and f({b}) = {fb} have the same sign. Regula Falsi requires a sign change."
            else:
                root, iterations, message = regula_falsi(f, a, b, tolerance, max_iter)
                
                if root is not None:
                    final_error = iterations[-1]['error'] if iterations and iterations[-1]['error'] is not None else 0
                    
                    result = {
                        'root': root,
                        'f_root': f(root),
                        'iterations': len(iterations),
                        'final_error': final_error,
                        'message': message
                    }
                    iterations_table = iterations
                    
                    step_by_step = generate_step_by_step(f, a, b, iterations, tolerance_percent)
                else:
                    error = message
                    
        except ValueError as e:
            error = f"Invalid input: {str(e)}"
        except Exception as e:
            error = f"Error: {str(e)}"
    
    return render_template('calculator.html', 
                         result=result, 
                         error=error, 
                         iterations=iterations_table, 
                         form_data=form_data,
                         step_by_step=step_by_step,
                         tolerance_percent=tolerance_percent)

if __name__ == '__main__':
    app.run(debug=True)