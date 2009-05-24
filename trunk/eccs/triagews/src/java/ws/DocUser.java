/*
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */

package ws;

/**
 *
 * @author Caballes
 */
public class DocUser {
    
    public boolean DocLoggedIn() {
        
        try { // Call Web Service Operation
            ws.DocUserService service = new ws.DocUserService();
            ws.DocU port = service.getDocUserPort();
            // TODO process result here
            boolean result = port.loggedIn();
            System.out.println("Result = "+result);
            
            if (result) {
                return true;
            }
        } catch (Exception ex) {
            // TODO handle custom exceptions here
        }
        
        return false;
    }
    
    public String getId() {
        
        java.lang.String result = "";
                
        try { // Call Web Service Operation
            ws.DocUserService service = new ws.DocUserService();
            ws.DocU port = service.getDocUserPort();
            // TODO process result here
            result = port.getDocid();
            System.out.println("Result = "+result);
        } catch (Exception ex) {
            // TODO handle custom exceptions here
        }

        return result;
    }
    
    public String getUser() {
        
        java.lang.String result = "";
                
        try { // Call Web Service Operation
            ws.DocUserService service = new ws.DocUserService();
            ws.DocU port = service.getDocUserPort();
            // TODO process result here
            result = port.getUsername();
            System.out.println("Result = "+result);
        } catch (Exception ex) {
            // TODO handle custom exceptions here
        }

        return result;
    }
    
    public void reset() {
        
        try { // Call Web Service Operation
            ws.DocUserService service = new ws.DocUserService();
            ws.DocU port = service.getDocUserPort();
            // TODO process result here
            port.resetUser();
        } catch (Exception ex) {
            // TODO handle custom exceptions here
        }
    }

}
